"""extra transplant columns

Revision ID: 03fb4c586089
Revises: 8c976165517c
Create Date: 2019-02-21 11:02:59.458000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '03fb4c586089'
down_revision = '8c976165517c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('transplants', sa.Column('date_of_cmv_infection', sa.Date(), nullable=True))
    op.add_column('transplants', sa.Column('donor_hla', sa.String(), nullable=True))
    op.add_column('transplants', sa.Column('recipient_hla', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('transplants', 'recipient_hla')
    op.drop_column('transplants', 'donor_hla')
    op.drop_column('transplants', 'date_of_cmv_infection')
    # ### end Alembic commands ###
