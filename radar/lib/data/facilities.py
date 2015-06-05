from radar.lib.database import db
from radar.models import Facility


def create_radar_facility():
    radar_facility = Facility(code='RADAR', name='RADAR', is_internal=True)
    db.session.add(radar_facility)
