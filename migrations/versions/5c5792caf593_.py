"""empty message

Revision ID: 5c5792caf593
Revises: 13a3da0db2d2
Create Date: 2016-03-12 16:14:17.557226

"""

# revision identifiers, used by Alembic.
revision = '5c5792caf593'
down_revision = '13a3da0db2d2'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('admin_fee',
    sa.Column('object_id', sa.Integer(), nullable=False),
    sa.Column('amount', sa.Integer(), nullable=False),
    sa.Column('reason', sa.UnicodeText(), nullable=False),
    sa.Column('paid', sa.Boolean(), nullable=False),
    sa.Column('charged_to_id', sa.Integer(), nullable=False),
    sa.Column('charged_by_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['charged_by_id'], [u'user.object_id'], ),
    sa.ForeignKeyConstraint(['charged_to_id'], [u'user.object_id'], ),
    sa.PrimaryKeyConstraint('object_id')
    )
    op.create_table('admin_fee_transaction_item',
    sa.Column('object_id', sa.Integer(), nullable=False),
    sa.Column('is_refund', sa.Boolean(), nullable=False),
    sa.Column('admin_fee_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['admin_fee_id'], [u'admin_fee.object_id'], ),
    sa.ForeignKeyConstraint(['object_id'], [u'transaction_item.object_id'], ),
    sa.PrimaryKeyConstraint('object_id')
    )
    op.add_column(u'log', sa.Column('admin_fee_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'log', 'admin_fee', ['admin_fee_id'], ['object_id'])
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'log', type_='foreignkey')
    op.drop_column(u'log', 'admin_fee_id')
    op.drop_table('admin_fee_transaction_item')
    op.drop_table('admin_fee')
    ### end Alembic commands ###