from radar.models.consultants import Consultant, GroupConsultant, Specialty
from radar.models.groups import Group, GROUP_TYPE

from radar_fixtures.utils import (
    generate_gender,
    generate_first_name,
    generate_last_name,
    add
)


specialties = ['Nephrologist']


def create_specialities():
    for name in specialties:
        specialty = Specialty()
        specialty.name = name
        add(specialty)


def create_consultants():
    create_specialities()

    specialty = Specialty.query.first()

    for group in Group.query.filter(Group.type == GROUP_TYPE.HOSPITAL).all():
        consultant = Consultant()
        gender = generate_gender()
        consultant.first_name = generate_first_name(gender)
        consultant.last_name = generate_last_name()
        consultant.specialty = specialty
        add(consultant)

        group_consultant = GroupConsultant()
        group_consultant.group = group
        group_consultant.consultant = consultant
        add(group_consultant)
