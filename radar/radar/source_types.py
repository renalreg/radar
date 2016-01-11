from radar.models.source_types import SourceType, SOURCE_TYPE_RADAR


def get_radar_source_type():
    return SourceType.query.get(SOURCE_TYPE_RADAR)


def is_radar_source_type(source_type):
    return source_type.id == SOURCE_TYPE_RADAR
