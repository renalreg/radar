from radar.models.groups import Group, GROUP_TYPE

from radar_fixtures.utils import add

HOSPITALS = [
    ('SPRINGFIELD', 'Springfield General Hospital'),
    ('CALMWOOD', 'Calmwood Mental Hospital'),
]


def create_hospitals():
    for code, name in HOSPITALS:
        group = Group()
        group.type = GROUP_TYPE.HOSPITAL
        group.code = code
        group.name = name
        group.short_name = name
        add(group)
