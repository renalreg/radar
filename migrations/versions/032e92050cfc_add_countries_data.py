"""add countries data

Revision ID: 032e92050cfc
Revises: 68e770e3b9b6
Create Date: 2017-03-15 13:38:07.646293

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '032e92050cfc'
down_revision = '68e770e3b9b6'
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    session = Session(bind=bind)
    countries = [Country(code=code, label=label) for code, label in COUNTRIES.items()]
    session.add_all(countries)
    session.commit()


def downgrade():
    op.execute('truncate table countries')

