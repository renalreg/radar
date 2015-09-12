from radar.lib.models import ORGANISATION_CODE_RADAR, Organisation, ORGANISATION_TYPE_OTHER, ORGANISATION_CODE_NHS, \
    ORGANISATION_CODE_CHI


def get_organisation(type, code):
    return Organisation.query\
        .filter(Organisation.type == type)\
        .filter(Organisation.code == code)\
        .one()


def get_radar_organisation():
    return get_organisation(ORGANISATION_TYPE_OTHER, ORGANISATION_CODE_RADAR)


def get_nhs_organisation():
    return get_organisation(ORGANISATION_TYPE_OTHER, ORGANISATION_CODE_NHS)


def get_chi_organisation():
    return get_organisation(ORGANISATION_TYPE_OTHER, ORGANISATION_CODE_CHI)
