"""bio-markers

Revision ID: d25d543b7787
Revises: 4a8a5a6428c9
Create Date: 2021-10-22 14:17:39.050945

"""
from sqlalchemy.sql.schema import ForeignKey
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "d25d543b7787"
down_revision = "4a8a5a6428c9"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "biomarkers",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("type", sa.String(100)),
    )
    op.create_table(
        "biomarker_results",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("pat_id", sa.Integer, ForeignKey("patients.id")),
        sa.Column("bio_id", sa.Integer, ForeignKey("biomarkers.id")),
        sa.Column("sample_id", sa.String(100)),
        sa.Column("barcode", sa.String(100)),
        sa.Column("value", sa.Float),
    )


def downgrade():
    op.drop_table("biomarker_results")
    op.drop_table("biomarkers")
