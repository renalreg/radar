"""Add nationality and ethnicity to a patient

Revision ID: 72c21b8fa484
Revises: a766a223a844
Create Date: 2017-03-16 14:19:07.185407

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '72c21b8fa484'
down_revision = 'a766a223a844'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('patient_demographics', sa.Column('ethnicity_id', sa.Integer(), nullable=True))
    op.add_column('patient_demographics', sa.Column('nationality_id', sa.Integer(), nullable=True))
    op.execute('update patient_demographics set ethnicity_id = (select id from ethnicities where code = ethnicity)')
    op.create_foreign_key(
        'patient_demographics_ethnicities_fkey',
        'patient_demographics',
        'ethnicities',
        ['ethnicity_id'],
        ['id']
    )
    op.create_foreign_key(
        'patient_demographics_nationalities_fkey',
        'patient_demographics',
        'nationalities',
        ['nationality_id'],
        ['id']
    )
    op.drop_column('patient_demographics', 'ethnicity')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('patient_demographics', sa.Column('ethnicity', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_constraint('patient_demographics_nationalities_fkey', 'patient_demographics', type_='foreignkey')
    op.drop_constraint('patient_demographics_ethnicities_fkey', 'patient_demographics', type_='foreignkey')
    op.execute('update patient_demographics set ethnicity = (select code from ethnicities where id = ethnicity_id)')
    op.drop_column('patient_demographics', 'nationality_id')
    op.drop_column('patient_demographics', 'ethnicity_id')
    # ### end Alembic commands ###