"""empty message

Revision ID: 4c5a72833c0b
Revises: 63011b54e21d
Create Date: 2016-03-28 11:44:55.135873

"""

# revision identifiers, used by Alembic.
revision = "4c5a72833c0b"
down_revision = "63011b54e21d"

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column("postage", sa.Column("posted", sa.Boolean(), nullable=False))
    op.alter_column(
        "ticket",
        "price_",
        existing_type=mysql.INTEGER(display_width=11),
        nullable=False,
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "ticket", "price_", existing_type=mysql.INTEGER(display_width=11), nullable=True
    )
    op.drop_column("postage", "posted")
    ### end Alembic commands ###
