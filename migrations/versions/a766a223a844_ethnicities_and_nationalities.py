"""ethnicities and nationalities

Revision ID: a766a223a844
Revises: 6e34e92cec6f
Create Date: 2017-03-16 13:41:09.964392

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'a766a223a844'
down_revision = '6e34e92cec6f'
branch_labels = None
depends_on = None

from sqlalchemy.orm import sessionmaker
from radar.models.patient_codes import ETHNICITIES
from radar.models import Ethnicity
Session = sessionmaker()


def upgrade():
    op.create_table(
        'ethnicities',
        sa.Column('id', sa.Integer, nullable=False),
        sa.Column('code', sa.String(length=10)),
        sa.Column('label', sa.String),
        sa.PrimaryKeyConstraint('id')
    )
    bind = op.get_bind()
    session = Session(bind=bind)
    ethnicities = [Ethnicity(code=code, label=label) for code, label in ETHNICITIES.items()]
    session.add_all(ethnicities)
    session.commit()

    op.create_table(
        'country_ethnicities',
        sa.Column('id', sa.Integer, nullable=False),
        sa.Column('ethnicity_id', sa.Integer, sa.ForeignKey('ethnicities.id')),
        sa.Column('country_code', sa.String(length=2), sa.ForeignKey('countries.code')),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'nationalities',
        sa.Column('id', sa.Integer, nullable=False),
        sa.Column('label', sa.String),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'country_nationalities',
        sa.Column('id', sa.Integer, nullable=False),
        sa.Column('nationality_id', sa.Integer, sa.ForeignKey('nationalities.id')),
        sa.Column('country_code', sa.String(length=2), sa.ForeignKey('countries.code')),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('country_nationalities')
    op.drop_table('nationalities')
    op.drop_table('country_ethnicities')
    op.drop_table('ethnicities')
