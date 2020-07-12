"""email phone

Revision ID: 520e48678de5
Revises: 8d708e1e2f94
Create Date: 2020-07-04 13:29:23.807943

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '520e48678de5'
down_revision = '8d708e1e2f94'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('order_details', sa.Column('email_id', sa.String(), nullable=False))
    op.add_column('order_details', sa.Column('number', sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('order_details', 'number')
    op.drop_column('order_details', 'email_id')
    # ### end Alembic commands ###