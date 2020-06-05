"""add cause of death

Revision ID: bde1ebc338e2
Revises: 28899fb1d913
Create Date: 2020-06-03 08:07:33.347538

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bde1ebc338e2'
down_revision = '28899fb1d913'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('patient_demographics', sa.Column('cause_of_death', sa.String))


def downgrade():
    op.drop_column('patient_demographics', 'cause_of_death')
