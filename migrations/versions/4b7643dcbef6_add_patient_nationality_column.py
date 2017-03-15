"""add patient nationality column

Revision ID: 4b7643dcbef6
Revises: 5068aee46dbd
Create Date: 2017-03-09 14:49:29.645915

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4b7643dcbef6'
down_revision = '5068aee46dbd'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('patient_demographics', sa.Column('nationality_id', sa.Integer, sa.ForeignKey('nationalities.id')))


def downgrade():
    op.drop_column('patient_demographics', 'nationality_id')
