from radar.models.data_sources import DataSource, DATA_SOURCE_TYPE_RADAR
from radar.models.organisations import Organisation, ORGANISATION_CODE_RADAR, ORGANISATION_TYPE_OTHER


def get_radar_data_source():
    return DataSource.query\
        .join(DataSource.organisation)\
        .filter(DataSource.type == DATA_SOURCE_TYPE_RADAR)\
        .filter(Organisation.type == ORGANISATION_TYPE_OTHER)\
        .filter(Organisation.code == ORGANISATION_CODE_RADAR)\
        .one()


def is_radar_data_source(data_source):
    return data_source.type == DATA_SOURCE_TYPE_RADAR and \
        data_source.organisation.type == ORGANISATION_TYPE_OTHER and \
        data_source.organisation.code == ORGANISATION_CODE_RADAR
