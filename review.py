#!/usr/bin/env python2
"""Script to automate squashing a branch for review.

Prepares the current branch for review, by diffing it against an appropriate
base (chosen by 'git merge-base master'), creating a new branch from that base
and applying the diff as a patch and committing and pushing the changes. If the
branch has already been sent for review, patches the new changes onto the
existing review commit and pushes the changes
"""

from __future__ import unicode_literals
from __future__ import with_statement

import json
import os
import subprocess
import sys
import tempfile

CMD_GET_BRANCH = ["git", "rev-parse", "--abbrev-ref", "HEAD"]
CMD_ADD_ALL = ["git", "add", "--all"]
CMD_AMEND_COMMIT = ["git", "commit", "--amend", "--no-edit"]


def cmd_get_diffbase(review_target, branch):
    """Generate a command to find the appropriate diffbase.

    Finds the best common ancestor of |review_target| and |branch|.
    """
    return ["git", "merge-base", review_target, branch]


def cmd_get_sha(ref):
    """Generate a command to find the SHA-1 hash for |ref|."""
    return ["git", "rev-parse", ref]


def cmd_get_diff(base, target):
    """Generate a command to find the diff between |base| and |target|."""
    return ["git", "diff", base, target]


def cmd_change_branch(branch, new=False):
    """Generate a command to change branch, creating the branch if necessary."""
    cmd = ["git", "checkout"]

    if new:
        cmd.append("-b")

    cmd.append(branch)

    return cmd


def cmd_apply_patch(patchfile):
    """Generate a command to apply a patch file."""
    return ["git", "apply", patchfile]


def cmd_commit(message):
    """Generate a command to commit staged changes."""
    return ["git", "commit", "-m", message]


def cmd_push_review(remote):
    """Generate a command to psuh changes to |remote|."""
    return ["git", "push", remote]


def main():
    """Run the script."""
    try:
        with open(os.path.realpath(__file__)[:-3] + ".json") as file_handle:
            reviews = json.load(file_handle)
    except IOError as _:
        reviews = {}

    branch = subprocess.check_output(CMD_GET_BRANCH).strip()

    if branch == "HEAD":
        sys.stderr.write("Cannot review a non-branch\n")
        sys.exit(1)

    if branch in reviews:
        review_target = reviews[branch]["review_target"]
    else:
        if len(sys.argv) > 1:
            review_target = sys.argv[1]
        else:
            sys.stderr.write("Must specify review target branch.")
            sys.exit(1)

    if branch in reviews:
        diffbase = reviews[branch]["last_commit"]
    else:
        diffbase = subprocess.check_output(
            cmd_get_diffbase(review_target, branch)
        ).strip()

    temp = tempfile.NamedTemporaryFile(delete=False)

    temp.write(subprocess.check_output(cmd_get_diff(diffbase, branch)))

    temp.close()

    review_branch = "review_" + branch

    if branch in reviews:
        subprocess.call(cmd_change_branch(review_branch))
    else:
        subprocess.call(cmd_change_branch(diffbase))
        subprocess.call(cmd_change_branch(review_branch, True))

    subprocess.call(cmd_apply_patch(temp.name))
    subprocess.call(CMD_ADD_ALL)

    if branch in reviews:
        subprocess.call(CMD_AMEND_COMMIT)
    else:
        subprocess.call(cmd_commit(raw_input("Change description: ")))

    subprocess.call(cmd_push_review("review_" + review_target))

    os.unlink(temp.name)

    reviews[branch] = {
        "last_commit": subprocess.check_output(cmd_get_sha(branch)).strip(),
        "review_target": review_target,
    }

    with open(os.path.realpath(__file__)[:-3] + ".json", "w+") as file_handle:
        json.dump(reviews, file_handle)

    subprocess.call(cmd_change_branch(branch))


if __name__ == "__main__":
    main()
