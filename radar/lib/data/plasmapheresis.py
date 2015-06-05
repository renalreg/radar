from radar.lib.database import db
from radar.models import PlasmapheresisResponse

# TODO
PLASMAPHERESIS_RESPONSES = [
    'Foo',
    'Bar',
    'Baz',
]


def create_plasmapheresis_responses():
    for v in PLASMAPHERESIS_RESPONSES:
        plasmapheresis_response = PlasmapheresisResponse(label=v)
        db.session.add(plasmapheresis_response)
