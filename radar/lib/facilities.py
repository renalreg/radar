from radar.models.facilities import Facility


def get_radar_facility():
    return Facility.query.filter(Facility.code == 'RADAR').one()
