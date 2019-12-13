"""signed_off to int

Revision ID: 28899fb1d913
Revises: 1da683d8e7b0
Create Date: 2019-11-20 11:23:33.234667

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '28899fb1d913'
down_revision = '1da683d8e7b0'
branch_labels = None
depends_on = None


def upgrade():

    # New states for signed_off
    # NULL = Not applicable cohort
    # 0 = Not signed off
    # 1 = Nurture baseline data complete
    # 2 = Nurture baseline and follow up data complete
        
    ################### STEP ONE ###################
    #==============================================#

    # An error is thrown if the default is not cleared 
    # from the column before changing the type

    step1 = "ALTER TABLE patients\
             ALTER COLUMN signed_off\
             DROP DEFAULT"

    op.execute(step1)

    ################### STEP TWO ###################
    #==============================================#    

    # Alter column type from boolean to int
    # All True become 1
    # All False become 0

    op.alter_column('patients', 
                    'signed_off',
                    new_column_name='signed_off_state',
                    existing_type=sa.BOOLEAN(), 
                    type_=sa.Integer(),
                    server_default=None,                              
                    postgresql_using="signed_off::Integer",
                    nullable=True
                    )
                    
    
    
    ################### STEP THREE ##################
    #===============================================#
    
    # Turn all patients that were false into nulls
    # All 0's become Null

    step3 = 'UPDATE patients\
             SET signed_off_state = NULL\
             WHERE signed_off_state = 0'

    op.execute(step3)

    ################### STEP FOUR ###################
    #===============================================#

    # Nuture patients that didn't have data completness before set to not signed off
    # All nuture cohort Null's become 0's
    # Note: Check table groups for the nurture group_id value

    step4 = 'UPDATE patients\
             SET signed_off_state = 0\
             FROM group_patients\
             WHERE patients.id = group_patients.patient_id\
             AND group_patients.group_id = 141\
             AND (signed_off_state != 1 OR signed_off_state IS NULL)'
    
    op.execute(step4)


def downgrade():
    
    # State of signed-off after steps complete
    # 0's and 1's become false
    # 2's and 3's become true    
    
    ################### STEP ONE ###################
    #==============================================#

    # Nuture not signed off are grouped with non nuture cohort patients
    # All NULL's become 0's

    step1 = 'UPDATE patients\
             SET signed_off_state = 0\
             WHERE signed_off_state IS NULL'

    op.execute(step1)

    ################### STEP TWO ###################
    #==============================================#    

    # All nuture patients with any kind of data completeness
    # are grouped together
    # All 2's become 1

    step2 = 'UPDATE patients\
             SET signed_off_state = 1\
             WHERE signed_off_state = 2'

    op.execute(step2)
    
    
    ################### STEP THREE ##################
    #===============================================#
    
    # An error is thrown if the default is not cleared 
    # from the column before changing the type

    step3 = "ALTER TABLE patients\
             ALTER COLUMN signed_off_state\
             DROP DEFAULT"

    op.execute(step3)

    ################### STEP FOUR ###################
    #===============================================#

    # Alter column type from int to boolean
    # All 1's become True
    # All 0's become False

    op.alter_column('patients', 
                    'signed_off_state',
                    new_column_name='signed_off', 
                    existing_type=sa.Integer(), 
                    type_=sa.BOOLEAN(),
                    server_default=sa.text("false"),                    
                    postgresql_using='signed_off_state::boolean')
