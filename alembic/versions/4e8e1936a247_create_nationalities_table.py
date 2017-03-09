"""create nationalities table

Revision ID: 4e8e1936a247
Revises: 
Create Date: 2017-03-09 10:44:18.873248

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4e8e1936a247'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'nationalities',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(100), nullable=False, unique=True)
    )


def downgrade():
    op.drop_table('nationalities')
