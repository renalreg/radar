"""add primary flag to patient diagnoses

Revision ID: dd73a75ce20c
Revises: d7a47953addd
Create Date: 2018-02-07 09:33:12.130543

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dd73a75ce20c'
down_revision = 'd7a47953addd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('patient_diagnoses', sa.Column('primary', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('patient_diagnoses', 'primary')
    # ### end Alembic commands ###