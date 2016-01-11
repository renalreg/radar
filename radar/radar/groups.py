from radar.models.groups import Group, OTHER_RADAR, GROUP_TYPE_OTHER


def get_radar_group():
    return Group.query.filter(Group.code == OTHER_RADAR, Group.type == GROUP_TYPE_OTHER).one()


def is_radar_group(group):
    return group.code == OTHER_RADAR and group.type == GROUP_TYPE_OTHER
