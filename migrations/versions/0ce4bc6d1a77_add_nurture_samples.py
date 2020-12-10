"""add nurture samples

Revision ID: 0ce4bc6d1a77
Revises: bde1ebc338e2
Create Date: 2020-12-02 11:43:33.333935

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0ce4bc6d1a77'
down_revision = 'bde1ebc338e2'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'nurture_samples_urine',
        sa.Column('sample_id', sa.String(20), primary_key=True),
        sa.Column('sample_date' sa.DateTime(), nullable=False)
        sa.Column('radar_id', sa.String(20), nullable=False),
        sa.Column('albumin', sa.String(10)),
        sa.Column('creatinin', sa.String(10)),
        sa.Column('ins_state', sa.Integer()),
        sa.Column('comments_label', sa.String(50)),
        sa.Column('comments_sample', sa.String(50))),

    op.create_table(
        'nurture_samples_blood',
        sa.Column('sample_id', sa.String(20), primary_key=True),
        sa.Column('sample_date' sa.DateTime(), nullable=False)
        sa.Column('radar_id', sa.String(20), nullable=False),
        sa.Column('bnp', sa.String(10)),
        sa.Column('creat', sa.String(10)),
        sa.Column('crp', sa.String(10)),
        sa.Column('cyst', sa.String(10)),
        sa.Column('gdf15', sa.String(10)),
        sa.Column('trop', sa.String(10)),
        sa.Column('ins_state', sa.Integer()),
        sa.Column('comments_label', sa.String(50)),
        sa.Column('comments_sample', sa.String(50)))

def downgrade():
    op.drop_table(nurture_samples_urine)
    op.drop_table(nurture_samples_blood)
