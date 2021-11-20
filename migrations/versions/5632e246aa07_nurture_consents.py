"""nurture consents

Revision ID: 5632e246aa07
Revises: d25d543b7787
Create Date: 2021-11-16 15:24:18.779379

"""
from sqlalchemy.sql.schema import ForeignKey, ForeignKeyConstraint
from alembic import op
import sqlalchemy as sa
from datetime import datetime, timezone

# revision identifiers, used by Alembic.
revision = "5632e246aa07"
down_revision = "d25d543b7787"
branch_labels = None
depends_on = None


def upgrade():
    new_table = op.create_table(
        "nurture_data",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("patient_id", sa.Integer()),
        sa.Column("signed_off_state", sa.Integer()),
        sa.Column("blood_tests", sa.Boolean()),
        sa.Column("interviews", sa.Boolean()),
        sa.Column("created_user_id", sa.Integer(), nullable=False),
        sa.Column(
            "created_date",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("modified_user_id", sa.Integer(), nullable=False),
        sa.Column(
            "modified_date",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(
            ["patient_id"],
            ["patients.id"],
        ),
    )

    pat_query = """
        SELECT id, signed_off_state 
        FROM patients
        WHERE signed_off_state IS NOT null
    """

    conn = op.get_bind()
    cursor = conn.execute(pat_query)
    patients = cursor.fetchall()

    pat_states = [
        {
            "patient_id": int(pat[0]),
            "signed_off_state": int(pat[1]),
            "blood_tests": True,
            "interviews": True,
            "created_user_id": 1,
            "created_date": datetime.now(timezone.utc),
            "modified_user_id": 1,
            "modified_date": datetime.now(timezone.utc),
        }
        for pat in patients
    ]

    op.bulk_insert(new_table, pat_states)

    op.drop_column("patients", "signed_off_state")


def downgrade():

    pat_query = """
        SELECT id, signed_off_state 
        FROM nurture_data
    """

    conn = op.get_bind()
    cursor = conn.execute(pat_query)
    pats = cursor.fetchall()

    op.add_column(
        "patients", sa.Column("signed_off_state", sa.Integer(), nullable=True)
    )

    pat_states = [
        {
            "patient_id": pat[0],
            "signed_off_state": pat[1],
        }
        for pat in pats
    ]

    for pat_state in pat_states:
        op.execute(
            f"UPDATE patients SET signed_off_state = {pat_state['signed_off_state']} WHERE id = {pat_state['patient_id']}"
        )

    op.drop_table("nurture_data")
