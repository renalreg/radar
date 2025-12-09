"""Add diagnosis options to MembNeph

Revision ID: 0a1d6e065731
Revises: 9a4f6d3b8c2e
Create Date: 2025-12-08 12:55:54.812406

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0a1d6e065731'
down_revision = '9a4f6d3b8c2e'
branch_labels = None
depends_on = None


antibody_enum = sa.Enum(
    'Anti-PLA2R',
    'Anti-THSD7A',
    name='antibody_type_enum'
)



def upgrade():
    antibody_enum.create(op.get_bind(), checkfirst=True)
    op.add_column('patient_diagnoses', sa.Column('antibodies', antibody_enum, nullable=True))
    op.add_column('patient_diagnoses', sa.Column('proteinuria_positive_antibody', sa.Boolean(), nullable=True))



def downgrade():
    op.drop_column('patient_diagnoses', 'proteinuria_positive_antibody')
    op.drop_column('patient_diagnoses', 'antibodies')

    antibody_enum.drop(op.get_bind(), checkfirst=True)
