from radar.models.organisations import Organisation, OrganisationConsultant
from radar.models.consultants import Consultant
from radar_fixtures.utils import generate_gender, generate_title, generate_first_name, generate_last_name
from radar_fixtures.validation import validate_and_add


def create_consultants():
    for organisation in Organisation.query.all():
        consultant = Consultant()
        gender = generate_gender()
        consultant.title = generate_title(gender)
        consultant.first_name = generate_first_name(gender)
        consultant.last_name = generate_last_name()

        organisation_consultant = OrganisationConsultant()
        organisation_consultant.organisation = organisation
        consultant.organisation_consultants.append(organisation_consultant)

        validate_and_add(consultant)
