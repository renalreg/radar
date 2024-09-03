"""added opt out options

Revision ID: 9a4f6d3b8c2e
Revises: 64df87443b3e
Create Date: 2024-08-28 14:14:57.640960

"""


from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '9a4f6d3b8c2e'
down_revision = '64df87443b3e'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('patient_demographics', sa.Column('opt_out_surveys', sa.Boolean(), server_default=sa.false()))
    op.add_column('patient_demographics', sa.Column('opt_out_newsletters', sa.Boolean(), server_default=sa.false()))


def downgrade():
    op.drop_column('patient_demographics', 'opt_out_surveys')
    op.drop_column('patient_demographics', 'opt_out_newsletters')
