"""add tables for z_score data

Revision ID: b714c0c415a5
Revises: f377001df0cb
Create Date: 2023-05-19 12:36:23.776174

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b714c0c415a5'
down_revision = 'f377001df0cb'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'ethnicities',
        sa.Column('id', sa.Integer, nullable=False),
        sa.Column('code', sa.Float()),
        sa.Column('label', sa.String),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    pass
