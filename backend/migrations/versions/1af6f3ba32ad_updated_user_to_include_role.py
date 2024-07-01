"""updated user to include role

Revision ID: 1af6f3ba32ad
Revises: 9aca798d5fab
Create Date: 2024-07-01 22:24:47.580612

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1af6f3ba32ad'
down_revision = '9aca798d5fab'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('role', sa.String(length=50), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('role')

    # ### end Alembic commands ###