import logging

from radar.database import db
from radar.models.patient_addresses import PatientAddress
from radar.ukrdc_importer.serializers import AddressSerializer
from radar.ukrdc_importer.utils import (
    build_id,
    delete_list,
    get_import_group,
    get_import_user,
    unique_list,
    validate_list,
)
from radar.utils import get_path


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
        city = get_path(self.data, 'city', 'code')
        if not city:
            city = get_path(self.data, 'city', 'description')
        return city

    @property
    def state(self):
        return get_path(self.data, 'state', 'code')

    @property
    def country(self):
        return get_path(self.data, 'country', 'code')

    @property
    def zip(self):
        postcode = get_path(self.data, 'zip', 'code')
        if not postcode:
            postcode = get_path(self.data, 'zip', 'description')
        return postcode


def parse_addresses(sda_addresses,adapter):
    def log(index, sda_address, e):
        adapter.error('Ignoring invalid address index={index}, errors={errors}'.format(index=index, errors=e.flatten()))

    serializer = AddressSerializer()
    sda_addresses = validate_list(sda_addresses, serializer, invalid_f=log)
    sda_addresses = map(SDAAddress, sda_addresses)

    return sda_addresses


def unique_addresses(sda_addresses, adapter):
    def key(sda_address):
        return (sda_address.street, sda_address.zip)

    def log(sda_address):
        adapter.warning('Ignoring duplicate address')

    sda_addresses = unique_list(sda_addresses, key_f=key, duplicate_f=log)

    return sda_addresses


def get_address(address_id):
    return PatientAddress.query.get(address_id)


def get_addresses(patient):
    q = PatientAddress.query
    q = q.filter(PatientAddress.source_type == 'UKRDC')
    q = q.filter(PatientAddress.patient == patient)
    return q.all()


def sync_addresses(patient, addresses_to_keep, adapter):
    def log(address):
        adapter.info('Deleting address id={id}'.format(id=address.id))

    addresses = get_addresses(patient)
    delete_list(addresses, addresses_to_keep, delete_f=log)


def build_address_id(patient, sda_address):
    return build_id(
        patient.id,
        PatientAddress.__tablename__,
        sda_address.street,
        sda_address.zip
    )


def convert_addresses(patient, sda_addresses, adapter):
    source_group = get_import_group()
    user = get_import_user()

    addresses = list()

    for sda_address in sda_addresses:
        address_id = build_address_id(patient, sda_address)
        address = get_address(address_id)

        if address is None:
            adapter.info('Creating address id={id}'.format(id=address_id))
            address = PatientAddress(id=address_id)
        else:
            adapter.info('Updating address id={id}'.format(id=address_id))

        address.patient = patient
        address.source_group = source_group
        address.source_type = 'UKRDC'
        address.created_user = user
        address.modified_user = user

        address.from_date = sda_address.from_date
        address.to_date = sda_address.to_date
        address.address1 = sda_address.street
        address.address2 = sda_address.city
        address.address3 = sda_address.state
        address.address4 = sda_address.country
        address.postcode = sda_address.zip

        db.session.add(address)
        addresses.append(address)

    return addresses


def import_addresses(patient, sda_addresses, adapter):
    adapter.info('Importing addresses: %s', patient.id)

    sda_addresses = parse_addresses(sda_addresses, adapter)
    sda_addresses = unique_addresses(sda_addresses, adapter)
    addresses = convert_addresses(patient, sda_addresses, adapter)
    sync_addresses(patient, addresses, adapter)

    adapter.info('Imported {n} address(es)'.format(n=len(addresses)))
