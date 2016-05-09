from radar.models.groups import Group, GROUP_CODE_RADAR, GROUP_TYPE


def get_radar_group():
    return Group.query.filter(Group.code == GROUP_CODE_RADAR, Group.type == GROUP_TYPE.OTHER).one()


def is_radar_group(group):
    return group.code == GROUP_CODE_RADAR and group.type == GROUP_TYPE.OTHER
