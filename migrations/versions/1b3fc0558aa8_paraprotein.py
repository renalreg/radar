"""paraprotein

Revision ID: 1b3fc0558aa8
Revises: b714c0c415a5
Create Date: 2023-12-11 17:06:42.504666

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "1b3fc0558aa8"
down_revision = "b714c0c415a5"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("patient_diagnoses", sa.Column("paraprotein", sa.Boolean()))


def downgrade():
    op.drop_column("patient_diagnoses", "paraprotein")
