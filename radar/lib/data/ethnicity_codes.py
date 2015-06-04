from radar.lib.database import db
from radar.models import EthnicityCode

ETHNICITY_CODES = [
    ('A', 'White - British'),
    ('B', 'White - Irish'),
    ('C', 'Other White Background'),
    ('D', 'Mixed - White and Black Caribbean'),
    ('E', 'Mixed - White and Black African'),
    ('F', 'Mixed - White and Asian'),
    ('G', 'Other Mixed Background'),
    ('H', 'Asian or Asian British - Indian'),
    ('J', 'Asian or Asian British - Pakistani'),
    ('K', 'Asian or Asian British - Bangladeshi'),
    ('L', 'Other Asian Background'),
    ('M', 'Black Carribean'),
    ('N', 'Black African'),
    ('P', 'Other Black Background'),
    ('R', 'Chinese'),
    ('S', 'Other Ethnic Background'),
    ('Z', 'Refused / Not Stated'),
]


def create_ethnicity_codes():
    for k, v in ETHNICITY_CODES:
        ethnicity_code = EthnicityCode(id=k, label=v)
        db.session.add(ethnicity_code)
