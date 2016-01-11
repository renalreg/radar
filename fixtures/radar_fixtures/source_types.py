from radar_fixtures.validation import validate_and_add
from radar.models.source_types import SourceType, SOURCE_TYPE_RADAR, SOURCE_TYPE_UKRDC

SOURCE_TYPES = [
    (SOURCE_TYPE_RADAR, 'RaDaR'),
    (SOURCE_TYPE_UKRDC, 'UKRDC'),
]


def create_source_types():
    for id, name in SOURCE_TYPES:
        source_type = SourceType()
        source_type.id = id
        source_type.name = name
        validate_and_add(source_type)
