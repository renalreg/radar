from radar.data.validation import validate
from radar.database import db
from radar.models import Organisation, ORGANISATION_CODE_RADAR, ORGANISATION_TYPE_OTHER, ORGANISATION_TYPE_UNIT, \
    ORGANISATION_CODE_NHS, ORGANISATION_CODE_CHI, ORGANISATION_CODE_UKRR, ORGANISATION_CODE_HANDC, \
    ORGANISATION_CODE_UKRDC, ORGANISATION_CODE_NHSBT, ORGANISATION_CODE_BAPN

UNITS = [
    ('RNJ00', "Barts"),
    ('RP4', 'Great Ormond Street'),
    ('RJ121', "Guy's"),
    ('RJZ', "King's College"),
    ('REE01', 'Southmead'),

]

OTHER_ORGANISATIONS = [
    (ORGANISATION_CODE_RADAR, 'RaDaR'),
    (ORGANISATION_CODE_NHS, 'NHS'),
    (ORGANISATION_CODE_CHI, 'CHI'),
    (ORGANISATION_CODE_UKRR, 'UK Renal Registry'),
    (ORGANISATION_CODE_HANDC, 'H&C'),
    (ORGANISATION_CODE_UKRDC, 'UKRDC'),
    (ORGANISATION_CODE_NHSBT, 'NHS Blood and Transplant'),
    (ORGANISATION_CODE_BAPN, 'BAPN'),
]


def create_organisations():
    create_other_organisations()
    create_unit_organisations()


def create_other_organisations():
    for organisation_code, organisation_name in OTHER_ORGANISATIONS:
        organisation = Organisation()
        organisation.code = organisation_code
        organisation.type = ORGANISATION_TYPE_OTHER
        organisation.name = organisation_name
        organisation = validate(organisation)
        db.session.add(organisation)


def create_unit_organisations():
    for code, name in UNITS:
        organisation = Organisation()
        organisation.code = code
        organisation.type = ORGANISATION_TYPE_UNIT
        organisation.name = name
        organisation = validate(organisation)
        db.session.add(organisation)
