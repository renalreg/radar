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
        'z_score_constants',
        sa.Column('id', sa.Integer, nullable=False),
        sa.Column('age_months', sa.Float),
        sa.Column('male_l_weight', sa.Float),
        sa.Column('male_median_weight', sa.Float),
        sa.Column('male_s_weight', sa.Float),
        sa.Column('female_l_weight', sa.Float),
        sa.Column('female_median_weight', sa.Float),
        sa.Column('female_s_weight', sa.Float),
        sa.Column('male_l_height', sa.Float),
        sa.Column('male_median_height', sa.Float),
        sa.Column('male_s_height', sa.Float),
        sa.Column('female_l_height', sa.Float),
        sa.Column('female_median_height', sa.Float),
        sa.Column('female_s_height', sa.Float),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('z_score_constants')
