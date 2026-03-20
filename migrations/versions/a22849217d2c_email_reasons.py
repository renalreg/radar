"""email_reasons

Revision ID: a22849217d2c
Revises: c6413ac84577
Create Date: 2026-03-16 17:55:06.771710

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'a22849217d2c'
down_revision = 'c6413ac84577'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('patient_demographics', sa.Column('email_reason', sa.String(), nullable=True))



def downgrade():
    op.drop_column('patient_demographics', 'email_reason')

