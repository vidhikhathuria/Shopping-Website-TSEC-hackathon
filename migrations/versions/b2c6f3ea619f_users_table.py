"""users table

Revision ID: b2c6f3ea619f
Revises: f351f2ea8290
Create Date: 2020-07-03 11:36:58.635641

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b2c6f3ea619f'
down_revision = 'f351f2ea8290'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('order_details',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('buyer_id', sa.Integer(), nullable=False),
    sa.Column('seller_id', sa.Integer(), nullable=False),
    sa.Column('current_warehouse_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['current_warehouse_id'], ['warehouse.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('warehouse', sa.Column('location', sa.String(length=60), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('warehouse', 'location')
    op.drop_table('order_details')
    # ### end Alembic commands ###
