"""add completness field

Revision ID: 4f24b92626f4
Revises: 99da04e11317
Create Date: 2018-11-09 13:50:15.559357

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4f24b92626f4'
down_revision = '99da04e11317'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('patients', sa.Column('signed_off', sa.Boolean(), server_default=sa.text('false'), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('patients', 'signed_off')
    # ### end Alembic commands ###