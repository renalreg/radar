"""hla-mismatch

Revision ID: 46944ada7c1f
Revises: d498b815d2c2
Create Date: 2024-07-01 13:26:06.692942

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '46944ada7c1f'
down_revision = 'd498b815d2c2'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('transplants', sa.Column('mismatch_hla', sa.String(), nullable=True))


def downgrade():
    op.drop_column('transplants', 'mismatch_hla')
