"""extra transplant rejection column

Revision ID: 751044a5528a
Revises: 03fb4c586089
Create Date: 2019-02-21 12:38:30.071000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '751044a5528a'
down_revision = '03fb4c586089'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('transplant_rejections', sa.Column('graft_loss_cause', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('transplant_rejections', 'graft_loss_cause')
    # ### end Alembic commands ###
