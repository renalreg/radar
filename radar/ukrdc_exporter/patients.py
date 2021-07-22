import logging

from radar.models.groups import (
    GROUP_CODE_CHI,
    GROUP_CODE_HSC,
    GROUP_CODE_NHS,
    GROUP_TYPE
)
from radar.models.patient_addresses import PatientAddress
from radar.models.patient_aliases import PatientAlias
from radar.models.patient_codes import GENDERS
from radar.models.patient_numbers import PatientNumber
from radar.models.source_types import SOURCE_TYPE_MANUAL
from radar.utils import date_to_datetime


logger = logging.getLogger(__name__)


def export_name(rda_patient, patient):
    if patient.radar_first_name or patient.radar_last_name:
        rda_name = rda_patient['name'] = {}

        if patient.radar_first_name:
            rda_name['given_name'] = patient.radar_first_name

        if patient.radar_last_name:
            rda_name['family_name'] = patient.radar_last_name


def export_birth_time(sda_patient, patient):
    if patient.radar_date_of_birth:
        sda_patient['birth_time'] = date_to_datetime(
            patient.radar_date_of_birth,
            with_timezone=False
        )


def export_death_time(sda_patient, patient):
    if patient.radar_date_of_death:
        sda_patient['death_time'] = date_to_datetime(
            patient.radar_date_of_death,
            with_timezone=False
        )


def export_gender(sda_patient, patient):
    if patient.radar_gender is not None:
        gender = patient.radar_gender
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
    if patient.radar_ethnicity is not None:
        code = patient.radar_ethnicity.code
        description = patient.radar_ethnicity.label

        if description is None:
            logger.error('Unknown ethnicity code={}'.format(code))
            return

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
    q = q.filter(PatientAlias.source_type == SOURCE_TYPE_MANUAL)
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
    q = q.filter(PatientAddress.source_type == SOURCE_TYPE_MANUAL)
    addresses = q.all()

    if not addresses:
        return

    sda_addresses = sda_patient.setdefault('addresses', list())

    for address in addresses:
        lines = [
            address.address1, address.address2,
            address.address3, address.address4
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


def export_patient_numbers(rda_patient, patient, groups):
    q = PatientNumber.query
    q = q.filter(PatientNumber.patient == patient)
    q = q.filter(PatientNumber.source_type == SOURCE_TYPE_MANUAL)
    patient_numbers = q.all()

    rda_patient_numbers = rda_patient.setdefault('patient_numbers', [])

    national_identifiers = {
        (GROUP_TYPE.OTHER, GROUP_CODE_NHS),
        (GROUP_TYPE.OTHER, GROUP_CODE_CHI),
        (GROUP_TYPE.OTHER, GROUP_CODE_HSC),
    }

    rda_patient_number = {
        'number': str(patient.id),
        'number_type': 'MRN',
        'organization': {
            'code': 'RADAR',
            'description': 'RaDaR'
        }
    }
    rda_patient_numbers.append(rda_patient_number)

    # Export national identifiers
    for patient_number in patient_numbers:
        key = (patient_number.number_group.type, patient_number.number_group.code)

        if key not in national_identifiers:
            continue

        rda_patient_number = {
            'number': patient_number.number,
            'number_type': 'NI',
            'organization': {
                'code': patient_number.number_group.code,
                'description': patient_number.number_group.name
            }
        }

        rda_patient_numbers.append(rda_patient_number)


def export_patient(rda_container, patient, groups):
    rda_patient = rda_container.setdefault('patient', {})
    export_name(rda_patient, patient)
    export_birth_time(rda_patient, patient)
    export_death_time(rda_patient, patient)
    export_gender(rda_patient, patient)
    export_patient_numbers(rda_patient, patient, groups)


# def export_patient(sda_container, patient, system_group):
#     sda_patient = sda_container.setdefault('patient', dict())
#     export_name(sda_patient, patient)
#     export_birth_time(sda_patient, patient)
#     export_death_time(sda_patient, patient)
#     export_gender(sda_patient, patient)
#     # export_ethnic_group(sda_patient, patient)
#     # export_contact_info(sda_patient, patient)
#     # export_aliases(sda_patient, patient)
#     # export_addresses(sda_patient, patient)
#     export_patient_numbers(sda_patient, patient, system_group)
