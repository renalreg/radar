"""fetal anon and renal imaging

Revision ID: f1399a1bd75a
Revises: 1b3fc0558aa8
Create Date: 2023-12-12 18:06:00.342319

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "f1399a1bd75a"
down_revision = "1b3fc0558aa8"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "fetal_anomaly_scans", sa.Column("right_mri_details", sa.String(10000))
    )
    op.add_column(
        "fetal_anomaly_scans", sa.Column("left_mri_details", sa.String(10000))
    )
    op.add_column("fetal_anomaly_scans", sa.Column("imaging_type", sa.String(50)))
    op.add_column(
        "renal_imaging", sa.Column("left_vesicoureteric_reflux", sa.Boolean())
    )
    op.add_column(
        "renal_imaging", sa.Column("left_hydronephrosis_hydroureter", sa.Boolean())
    )
    op.add_column(
        "renal_imaging", sa.Column("right_vesicoureteric_reflux", sa.Boolean())
    )
    op.add_column(
        "renal_imaging", sa.Column("right_hydronephrosis_hydroureter", sa.Boolean())
    )


def downgrade():
    op.drop_column("fetal_anomaly_scans", "right_mri_details")
    op.drop_column("fetal_anomaly_scans", "left_mri_details")
    op.drop_column("fetal_anomaly_scans", "imaging_type")
    op.drop_column("renal_imaging", "left_vesicoureteric_reflux")
    op.drop_column("renal_imaging", "left_hydronephrosis_hydroureter")
    op.drop_column("renal_imaging", "right_vesicoureteric_reflux")
    op.drop_column("renal_imaging", "right_hydronephrosis_hydroureter")
