"""pregnancy infant DOB

Revision ID: d498b815d2c2
Revises: f1399a1bd75a
Create Date: 2024-06-18 11:16:36.127384

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd498b815d2c2'
down_revision = 'f1399a1bd75a'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("pregnancies", sa.Column("infant_dob", sa.Date(), nullable=True))
    op.alter_column("pregnancies", "date_of_lmp", nullable=True)


def downgrade():
    op.drop_column("pregnancies", "infant_dob")
    op.alter_column("pregnancies", "date_of_lmp", nullable=False)
