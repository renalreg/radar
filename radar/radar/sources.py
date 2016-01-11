from radar.models.sources import Source, SOURCE_RADAR


def get_radar_source():
    return Source.query.get(SOURCE_RADAR)


def is_radar_source(source):
    return source.id == SOURCE_RADAR
