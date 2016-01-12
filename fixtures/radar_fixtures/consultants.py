from radar.models.consultants import Consultant
from radar_fixtures.utils import generate_gender, generate_first_name, generate_last_name
from radar_fixtures.validation import validate_and_add
from radar.models.groups import Group, GROUP_TYPE_HOSPITAL
from radar.models.consultants import GroupConsultant


def create_consultants():
    for group in Group.query.filter(Group.type == GROUP_TYPE_HOSPITAL).all():
        consultant = Consultant()
        gender = generate_gender()
        consultant.first_name = generate_first_name(gender)
        consultant.last_name = generate_last_name()

        group_consultant = GroupConsultant()
        group_consultant.group = group
        consultant.group_consultants.append(group_consultant)

        validate_and_add(consultant)
