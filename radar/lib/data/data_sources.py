from radar.lib.data.validation import validate_data_source
from radar.lib.data_sources import DATA_SOURCE_TYPE_RADAR
from radar.lib.database import db
from radar.lib.models import DataSource, ORGANISATION_TYPE_UNIT, Organisation, DATA_SOURCE_TYPE_PV
from radar.lib.organisations import get_radar_organisation


def create_data_sources():
    create_radar_data_source()
    create_unit_data_sources()


def create_radar_data_source():
    data_source = DataSource()
    data_source.organisation = get_radar_organisation()
    data_source.type = DATA_SOURCE_TYPE_RADAR
    data_source = validate_data_source(data_source)
    db.session.add(data_source)


def create_unit_data_sources():
    units = Organisation.query.filter(Organisation.type == ORGANISATION_TYPE_UNIT)

    for data_source_type in [DATA_SOURCE_TYPE_RADAR, DATA_SOURCE_TYPE_PV]:
        for unit in units:
            data_source = DataSource()
            data_source.organisation = unit
            data_source.type = data_source_type
            data_source = validate_data_source(data_source)
            db.session.add(data_source)
