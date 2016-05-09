from radar.models.consultants import Consultant, GroupConsultant
from radar.models.groups import Group, GROUP_TYPE

from radar_fixtures.utils import (
    generate_gender,
    generate_first_name,
    generate_last_name,
    add
)


def create_consultants():
    for group in Group.query.filter(Group.type == GROUP_TYPE.HOSPITAL).all():
        consultant = Consultant()
        gender = generate_gender()
        consultant.first_name = generate_first_name(gender)
        consultant.last_name = generate_last_name()
        add(consultant)

        group_consultant = GroupConsultant()
        group_consultant.group = group
        group_consultant.consultant = consultant
        add(group_consultant)
