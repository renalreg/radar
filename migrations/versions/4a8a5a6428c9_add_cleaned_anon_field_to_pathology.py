"""add cleaned anon field to pathology

Revision ID: 4a8a5a6428c9
Revises: 0ce4bc6d1a77
Create Date: 2021-01-15 13:50:02.766442

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4a8a5a6428c9'
down_revision = '0ce4bc6d1a77'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('pathology', sa.Column('report_cleaned', sa.Date(), nullable=True))


def downgrade():
    op.drop_column('pathology', 'report_cleaned')
