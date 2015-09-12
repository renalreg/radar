from radar.lib.database import db
from radar.lib.models import Organisation, ORGANISATION_CODE_RADAR, ORGANISATION_TYPE_OTHER, ORGANISATION_TYPE_UNIT, \
    ORGANISATION_CODE_NHS, ORGANISATION_CODE_CHI


# TODO
# http://en.wikipedia.org/wiki/List_of_fictional_institutions#Hospitals
UNITS = [
    ('A', 'All Saints Hospital'),
    ('B', 'Chelsea General Hospital'),
    ('C', 'Chicago Hope'),
    ('D', 'County General Hospital'),
    ('E', 'Community General Hospital'),
]


def create_organisations():
    create_radar_organisation()
    create_nhs_organisation()
    create_chi_organisation()
    create_unit_organisations()


def create_radar_organisation():
    organisation = Organisation()
    organisation.code = ORGANISATION_CODE_RADAR
    organisation.type = ORGANISATION_TYPE_OTHER
    organisation.name = 'RaDaR'
    db.session.add(organisation)


def create_nhs_organisation():
    organisation = Organisation()
    organisation.code = ORGANISATION_CODE_NHS
    organisation.type = ORGANISATION_TYPE_OTHER
    organisation.name = 'NHS'
    db.session.add(organisation)


def create_chi_organisation():
    organisation = Organisation()
    organisation.code = ORGANISATION_CODE_CHI
    organisation.type = ORGANISATION_TYPE_OTHER
    organisation.name = 'CHI'
    db.session.add(organisation)


def create_unit_organisations():
    for code, name in UNITS:
        organisation = Organisation()
        organisation.code = code
        organisation.type = ORGANISATION_TYPE_UNIT
        organisation.name = name
        db.session.add(organisation)
