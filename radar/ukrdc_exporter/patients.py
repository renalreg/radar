import logging

from radar.models.groups import (
    GROUP_CODE_NHS,
    GROUP_CODE_CHI,
    GROUP_CODE_HSC,
    GROUP_TYPE
)
from radar.models.patient_addresses import PatientAddress
from radar.models.patient_aliases import PatientAlias
from radar.models.patient_numbers import PatientNumber
from radar.models.patients import GENDERS, ETHNICITIES


logger = logging.getLogger(__name__)


def export_name(sda_patient, patient):
    if patient.first_name or patient.last_name:
        sda_name = sda_patient['name'] = dict()

        if patient.first_name:
            sda_name['given_name'] = patient.first_name

        if patient.last_name:
            sda_name['family_name'] = patient.last_name


def export_birth_time(sda_patient, patient):
    if patient.date_of_birth:
        sda_patient['birth_time'] = patient.date_of_birth


def export_death_time(sda_patient, patient):
    if patient.date_of_death:
        sda_patient['death_time'] = patient.date_of_death


def export_gender(sda_patient, patient):
    if patient.gender is not None:
        gender = patient.gender
        description = GENDERS.get(gender)

        if description is None:
            logger.error('Unknown gender code={}'.format(gender))
            return

        code = str(gender)

        sda_patient['gender'] = {
            'code': code,
            'description': description
        }


def export_ethnic_group(sda_patient, patient):
    if patient.ethnicity is not None:
        ethnicity = patient.ethnicity
        description = ETHNICITIES.get(ethnicity)

        if description is None:
            logger.error('Unknown ethnicity code={}'.format(ethnicity))
            return

        code = str(ethnicity)

        sda_patient['ethnic_group'] = {
            'code': code,
            'description': description
        }


def export_contact_info(sda_patient, patient):
    if (
        patient.home_number or
        patient.work_number or
        patient.mobile_number or
        patient.email_address
    ):
        sda_contact_info = sda_patient['contact_info'] = dict()

        if patient.home_number:
            sda_contact_info['home_phone_number'] = patient.home_number

        if patient.work_number:
            sda_contact_info['work_phone_number'] = patient.work_number

        if patient.mobile_number:
            sda_contact_info['mobile_phone_number'] = patient.mobile_number

        if patient.email_address:
            sda_contact_info['email_address'] = patient.email_address


def export_aliases(sda_patient, patient):
    q = PatientAlias.query
    q = q.filter(PatientAlias.patient == patient)
    q = q.filter(PatientAlias.source_type == 'RADAR')
    aliases = q.all()

    if not aliases:
        return

    sda_aliases = sda_patient.setdefault('aliases', list())

    for alias in aliases:
        if not alias.first_name and not alias.last_name:
            continue

        sda_name = {}

        if alias.first_name:
            sda_name['given_name'] = alias.first_name

        if alias.last_name:
            sda_name['family_name'] = alias.last_name

        sda_aliases.append(sda_name)


def export_addresses(sda_patient, patient):
    q = PatientAddress.query
    q = q.filter(PatientAddress.patient == patient)
    q = q.filter(PatientAddress.source_type == 'RADAR')
    addresses = q.all()

    if not addresses:
        return

    sda_addresses = sda_patient.setdefault('addresses', list())

    for address in addresses:
        lines = [
            address.address_1, address.address_2,
            address.address_3, address.address_4
        ]

        street = '; '.join(line for line in lines if line)

        if not street and not address.postcode:
            continue

        sda_address = dict()

        if street:
            sda_address['street'] = street

        if address.postcode:
            sda_address['zip'] = {
                'code': address.postcode,
                'description': address.postcode,
            }

        sda_addresses.append(sda_address)


def export_patient_numbers(sda_patient, patient, group):
    q = PatientNumber.query
    q = q.filter(PatientNumber.patient == patient)
    q = q.filter(PatientNumber.source_type == 'RADAR')
    patient_numbers = q.all()

    sda_patient_numbers = sda_patient.setdefault('patient_numbers', list())

    # The SDA must include a MRN otherwise all patients will be grouped under a NULL MRN
    # The MRN must appear first in the list of numbers as the organization code is used as the facility
    sda_patient_number = {
        'number': str(patient.id),
        'number_type': 'MRN',
        'organization': {
            'code': 'RADAR',
            'description': 'RaDaR'
        }
    }
    sda_patient_numbers.append(sda_patient_number)

    national_identifiers = {
        (GROUP_TYPE.OTHER, GROUP_CODE_NHS),
        (GROUP_TYPE.OTHER, GROUP_CODE_CHI),
        (GROUP_TYPE.OTHER, GROUP_CODE_HSC),
    }

    # Export national identifiers
    for patient_number in patient_numbers:
        key = (patient_number.number_group.type, patient_number.number_group.code)

        if key not in national_identifiers:
            continue

        sda_patient_number = {
            'number': patient_number.number,
            'number_type': 'NI',
            'organization': {
                'code': patient_number.number_group.code,
                'description': patient_number.number_group.name
            }
        }

        sda_patient_numbers.append(sda_patient_number)


def export_patient(sda_container, patient, group):
    sda_patient = sda_container.setdefault('patient', dict())
    export_name(sda_patient, patient)
    export_birth_time(sda_patient, patient)
    export_death_time(sda_patient, patient)
    export_gender(sda_patient, patient)
    export_ethnic_group(sda_patient, patient)
    export_contact_info(sda_patient, patient)
    export_aliases(sda_patient, patient)
    export_addresses(sda_patient, patient)
    export_patient_numbers(sda_patient, patient, group)
