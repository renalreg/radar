from radar.lib.models import ORGANISATION_CODE_RADAR, Organisation, ORGANISATION_TYPE_OTHER, ORGANISATION_CODE_NHS, \
    ORGANISATION_CODE_CHI, ORGANISATION_CODE_UKRR, ORGANISATION_CODE_HANDC


def get_organisation(type, code):
    return Organisation.query\
        .filter(Organisation.type == type)\
        .filter(Organisation.code == code)\
        .one()


def get_radar_organisation():
    return get_organisation(ORGANISATION_TYPE_OTHER, ORGANISATION_CODE_RADAR)


def get_ukrr_organisation():
    return get_organisation(ORGANISATION_TYPE_OTHER, ORGANISATION_CODE_UKRR)


def get_nhs_organisation():
    return get_organisation(ORGANISATION_TYPE_OTHER, ORGANISATION_CODE_NHS)


def get_chi_organisation():
    return get_organisation(ORGANISATION_TYPE_OTHER, ORGANISATION_CODE_CHI)


def get_handc_organisation():
    return get_organisation(ORGANISATION_TYPE_OTHER, ORGANISATION_CODE_HANDC)


def is_radar_organisation(organisation):
    return organisation.code == ORGANISATION_CODE_RADAR and organisation.type == ORGANISATION_TYPE_OTHER


def is_ukrr_organisation(organisation):
    return organisation.code == ORGANISATION_CODE_UKRR and organisation.type == ORGANISATION_TYPE_OTHER


def is_handc_organisation(organisation):
    return organisation.code == ORGANISATION_CODE_HANDC and organisation.type == ORGANISATION_TYPE_OTHER


def is_nhs_organisation(organisation):
    return organisation.code == ORGANISATION_CODE_NHS and organisation.type == ORGANISATION_TYPE_OTHER


def is_chi_organisation(organisation):
    return organisation.code == ORGANISATION_CODE_CHI and organisation.type == ORGANISATION_TYPE_OTHER
