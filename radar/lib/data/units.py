from radar.lib.database import db
from radar.models import Unit, Facility

# TODO
# http://en.wikipedia.org/wiki/List_of_fictional_institutions#Hospitals
UNITS = [
    ('A', 'All Saints Hospital'),
    ('B', 'Chelsea General Hospital'),
    ('C', 'Chicago Hope'),
    ('D', 'County General Hospital'),
    ('E', 'Community General Hospital'),
]


def create_units():
    for code, name in UNITS:
        unit = Unit(name=name)
        db.session.add(unit)

        facility = Facility(code=code, name=name, unit=unit, is_internal=True)
        db.session.add(facility)
