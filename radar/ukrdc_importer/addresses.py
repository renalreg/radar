import logging

from radar.models.patient_addresses import PatientAddress
from radar.database import db

from radar.ukrdc_importer.utils import (
    load_validator,
    validate_list,
    unique_list,
    delete_list,
    build_id,
    get_path,
    get_import_group,
    get_import_user,
    parse_datetime_path
)


logger = logging.getLogger(__name__)


class SDAAddress(object):
    def __init__(self, data):
        self.data = data

    @property
    def from_time(self):
        return self.data.get('from_time')

    @property
    def from_date(self):
        from_time = self.from_time

        if from_time is None:
            return None
        else:
            return from_time.date()

    @property
    def to_time(self):
        return self.data.get('to_time')

    @property
    def to_date(self):
        to_time = self.to_time

        if to_time is None:
            return None
        else:
            return to_time.date()

    @property
    def street(self):
        return get_path(self.data, 'street')

    @property
    def city(self):
        return get_path(self.data, 'city', 'code')

    @property
    def state(self):
        return get_path(self.data, 'state', 'code')

    @property
    def country(self):
        return get_path(self.data, 'country', 'code')

    @property
    def zip(self):
        return get_path(self.data, 'zip', 'code')


def parse_addresses(sda_addresses):
    def log(index, sda_address, error):
        logger.error('Ignoring invalid address index={index}'.format(index=index))

    validator = load_validator('address.json')
    sda_addresses = validate_list(sda_addresses, validator, invalid_f=log)

    for sda_address in sda_addresses:
        parse_datetime_path(sda_address, 'from_time')
        parse_datetime_path(sda_address, 'to_time')

    sda_addresses = map(SDAAddress, sda_addresses)

    return sda_addresses


def unique_addresses(sda_addresses):
    def key(sda_address):
        return (sda_address.street, sda_address.zip)

    def log(sda_address):
        logger.error('Ignoring duplicate address')

    sda_addresses = unique_list(sda_addresses, key_f=key, duplicate_f=log)

    return sda_addresses


def get_address(address_id):
    return PatientAddress.query.get(address_id)


def get_addresses(patient):
    q = PatientAddress.query
    q = q.filter(PatientAddress.source_type == 'UKRDC')
    q = q.filter(PatientAddress.patient == patient)
    return q.all()


def sync_addresses(patient, addresses_to_keep):
    def log(address):
        logger.info('Deleting address id={id}'.format(id=address.id))

    addresses = get_addresses(patient)
    delete_list(addresses, addresses_to_keep, delete_f=log)


def build_address_id(patient, sda_address):
    return build_id(
        patient.id,
        PatientAddress.__tablename__,
        sda_address.street,
        sda_address.zip
    )


def convert_addresses(patient, sda_addresses):
    source_group = get_import_group()
    user = get_import_user()

    addresses = list()

    for sda_address in sda_addresses:
        address_id = build_address_id(patient, sda_address)
        address = get_address(address_id)

        if address is None:
            logger.info('Creating address id={id}'.format(id=address_id))
            address = PatientAddress(id=address_id)
        else:
            logger.info('Updating address id={id}'.format(id=address_id))

        address.patient = patient
        address.source_group = source_group
        address.source_type = 'UKRDC'
        address.created_user = user
        address.modified_user = user

        address.from_date = sda_address.from_date
        address.to_date = sda_address.to_date
        address.address_1 = sda_address.street
        address.address_2 = sda_address.city
        address.address_3 = sda_address.state
        address.address_4 = sda_address.country
        address.postcode = sda_address.zip

        db.session.add(address)
        addresses.append(address)

    return addresses


def import_addresses(patient, sda_addresses):
    logger.info('Importing addresses')

    sda_addresses = parse_addresses(sda_addresses)
    sda_addresses = unique_addresses(sda_addresses)
    addresses = convert_addresses(patient, sda_addresses)
    sync_addresses(patient, addresses)

    logger.info('Imported {n} address(es)'.format(n=len(addresses)))
