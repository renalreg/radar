from radar.models import ORGANISATION_CODE_RADAR, Organisation, ORGANISATION_TYPE_OTHER, ORGANISATION_CODE_NHS, \
    ORGANISATION_CODE_CHI, ORGANISATION_CODE_UKRR, ORGANISATION_CODE_HANDC, ORGANISATION_CODE_UKRDC, \
    ORGANISATION_CODE_NHSBT


def get_organisation(type, code):
    return Organisation.query\
        .filter(Organisation.type == type)\
        .filter(Organisation.code == code)\
        .one()


def get_ukrdc_organisation():
    return get_other_organisation(ORGANISATION_CODE_UKRDC)


def get_radar_organisation():
    return get_other_organisation(ORGANISATION_CODE_RADAR)


def get_ukrr_organisation():
    return get_other_organisation(ORGANISATION_CODE_UKRR)


def get_nhs_organisation():
    return get_other_organisation(ORGANISATION_CODE_NHS)


def get_chi_organisation():
    return get_other_organisation(ORGANISATION_CODE_CHI)


def get_handc_organisation():
    return get_other_organisation(ORGANISATION_CODE_HANDC)


def get_nhsbt_organisation():
    return get_other_organisation(ORGANISATION_CODE_NHSBT)


def is_ukrdc_organisation(organisation):
    return is_other_organisation(organisation, ORGANISATION_CODE_UKRDC)


def is_radar_organisation(organisation):
    return is_other_organisation(organisation, ORGANISATION_CODE_RADAR)


def is_ukrr_organisation(organisation):
    return is_other_organisation(organisation, ORGANISATION_CODE_UKRR)


def is_handc_organisation(organisation):
    return is_other_organisation(organisation, ORGANISATION_CODE_HANDC)


def is_nhs_organisation(organisation):
    return is_other_organisation(organisation, ORGANISATION_CODE_NHS)


def is_chi_organisation(organisation):
    return is_other_organisation(organisation, ORGANISATION_CODE_CHI)


def is_nhsbt_organisation(organisation):
    return is_other_organisation(organisation, ORGANISATION_CODE_NHSBT)


def is_other_organisation(organisation, code):
    return organisation.code == code and organisation.type == ORGANISATION_TYPE_OTHER

    return get_organisation(ORGANISATION_TYPE_OTHER, code)


def get_other_organisation(code):
    return get_organisation(ORGANISATION_TYPE_OTHER, code)
