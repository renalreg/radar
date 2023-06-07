"""add comments field to ALPORT_CLINICAL_PICTURES

Revision ID: f377001df0cb
Revises: 5632e246aa07
Create Date: 2023-05-15 16:34:17.522517

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f377001df0cb'
down_revision = '5632e246aa07'
branch_labels = None
depends_on = None


def upgrade():    
    op.add_column('alport_clinical_pictures', sa.Column('comments', sa.String(), nullable=True))


def downgrade():
    op.drop_column('alport_clinical_pictures', 'comments')
