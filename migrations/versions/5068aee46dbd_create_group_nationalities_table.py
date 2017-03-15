"""create group nationalities table

Revision ID: 5068aee46dbd
Revises: 4e8e1936a247
Create Date: 2017-03-09 13:17:37.381699

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5068aee46dbd'
down_revision = '4e8e1936a247'
branch_labels = None
depends_on = None


table_name = 'group_nationalities'


def upgrade():
    op.create_table(
        table_name,
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('group_id', sa.Integer, sa.ForeignKey('groups.id')),
        sa.Column('nationality_id', sa.Integer, sa.ForeignKey('nationalities.id'))
    )


def downgrade():
    op.drop_table(table_name)
