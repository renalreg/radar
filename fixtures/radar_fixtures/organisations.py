from radar_fixtures.validation import validate_and_add
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
    (ORGANISATION_CODE_RADAR, 'RaDaR', True),
    (ORGANISATION_CODE_NHS, 'NHS', True),
    (ORGANISATION_CODE_CHI, 'CHI', True),
    (ORGANISATION_CODE_UKRR, 'UK Renal Registry', True),
    (ORGANISATION_CODE_HANDC, 'H&C', True),
    (ORGANISATION_CODE_UKRDC, 'UKRDC', True),
    (ORGANISATION_CODE_NHSBT, 'NHS Blood and Transplant', True),
    (ORGANISATION_CODE_BAPN, 'BAPN', True),
]


def create_organisations():
    create_other_organisations()
    create_unit_organisations()


def create_other_organisations():
    for code, name, recruitment in OTHER_ORGANISATIONS:
        organisation = Organisation()
        organisation.code = code
        organisation.type = ORGANISATION_TYPE_OTHER
        organisation.name = name
        organisation.recruitment = recruitment
        validate_and_add(organisation)


def create_unit_organisations():
    for code, name in UNITS:
        organisation = Organisation()
        organisation.code = code
        organisation.type = ORGANISATION_TYPE_UNIT
        organisation.name = name
        organisation.recruitment = False
        validate_and_add(organisation)
