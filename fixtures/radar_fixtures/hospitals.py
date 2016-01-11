from radar_fixtures.validation import validate_and_add
from radar.models.groups import Group, GROUP_TYPE_HOSPITAL

HOSPITALS = [
    ("RNJ00", "Barts"),
    ("RP4", 'Great Ormond Street'),
    ("RJ121", "Guy's"),
    ("RJZ", "King's College"),
    ("REE01", 'Southmead'),
]


def create_hospitals():
    for code, name in HOSPITALS:
        group = Group()
        group.type = GROUP_TYPE_HOSPITAL
        group.code = code
        group.name = name
        group.short_name = name
        validate_and_add(group)
