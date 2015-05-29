from radar.models.facilities import Facility
from radar.lib.sda.models import SDABundle, SDAPatient, SDAPatientAddress, SDAPatientAlias
from radar.lib.utils import set_path


def demographics_to_sda_bundle(demographics):
    # TODO
    facility = Facility.query.filter(Facility.code == 'RADAR').first_or_404()

    sda_bundle = SDABundle(facility=facility, patient=demographics.patient)

    sda_patient = SDAPatient()

    if demographics.gender == 1:
        gender_code = 'M'
        gender_description = 'Male'
    else:
        gender_code = 'F'
        gender_description = 'Male'

    sda_patient.data = {
        'name': {
            'given_name': demographics.first_name,
            'family_name': demographics.last_name,
        },
        'birth_time': demographics.date_of_birth,
        'gender': {
            'code': gender_code,
            'description': gender_description,
        }
    }

    if demographics.date_of_death:
        sda_patient.data['death_time'] = demographics.date_of_death

    sda_bundle.sda_patient = sda_patient

    sda_patient_address = SDAPatientAddress()

    sda_patient_address.data = {
        'zip': {
            'description': demographics.postcode
        }
    }

    street = '; '.join(x for x in [demographics.address_line_1, demographics.address_line_2, demographics.address_line_3] if x)

    if street:
        sda_patient_address.data['street'] = street

    sda_patient.addresses.append(sda_patient_address)

    if demographics.home_number:
        set_path(sda_patient.data, ['contact_info', 'home_phone_number'], demographics.home_number)

    if demographics.work_number:
        set_path(sda_patient.data, ['contact_info', 'work_phone_number'], demographics.work_number)

    if demographics.mobile_number:
        set_path(sda_patient.data, ['contact_info', 'mobile_phone_number'], demographics.mobile_number)

    if demographics.email_address:
        set_path(sda_patient.data, ['contact_info', 'email_address'], demographics.email_address)

    if demographics.alias_first_name or demographics.alias_last_name:
        sda_patient_alias = SDAPatientAlias()
        sda_patient_alias.data = {}

        if demographics.alias_first_name:
            sda_patient_alias.data['given_name'] = demographics.first_name

        if demographics.alias_last_name:
            sda_patient_alias.data['family_name'] = demographics.last_name

        sda_patient.aliases.append(sda_patient_alias)

    return sda_bundle