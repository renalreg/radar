import logging

from radar.database import db
from radar.models.medications import Medication
from radar.ukrdc_importer.serializers import MedicationSerializer
from radar.ukrdc_importer.utils import (
    build_id,
    delete_list,
    get_group,
    get_import_user,
    unique_list,
    validate_list,
)
from radar.utils import get_path


logger = logging.getLogger(__name__)


class SDAMedication(object):
    def __init__(self, data):
        self.data = data

    @property
    def external_id(self):
        return self.data['external_id']

    @property
    def from_time(self):
        return self.data['from_time']

    @property
    def from_date(self):
        return self.from_time.date()

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
    def order_item_description(self):
        return get_path(self.data, 'order_item', 'description')

    @property
    def dose_uom(self):
        return (
            get_path(self.data, 'dose_uom', 'code') or
            get_path(self.data, 'dose_uom', 'description')
        )

    @property
    def entering_organization(self):
        return (
            get_path(self.data, 'entering_organization', 'organization', 'code') or
            get_path(self.data, 'entering_organization', 'code')
        )

    @property
    def entered_at(self):
        return get_path(self.data, 'entered_at', 'code')


def parse_medications(sda_medications):
    def log(index, sda_medication, e):
        logger.error(
            'Ignoring invalid medication index={index}, errors={errors}'.format(
                index=index,
                errors=e.flatten()
            )
        )

    serializer = MedicationSerializer()
    sda_medications = validate_list(sda_medications, serializer, invalid_f=log)
    sda_medications = map(SDAMedication, sda_medications)

    return sda_medications


def unique_medications(sda_medications):
    def key(sda_medication):
        return sda_medication.external_id

    def log(sda_medication):
        external_id = sda_medication.external_id
        logger.error('Ignoring duplicate medication external_id={external_id}'.format(external_id))

    sda_medications = unique_list(sda_medications, key_f=key, duplicate_f=log)

    return sda_medications


def preload_medications(patient):
    get_medications(patient)


def get_medication(medication_id):
    return Medication.query.get(medication_id)


def get_medications(patient):
    q = Medication.query
    q = q.filter(Medication.source_type == 'UKRDC')
    q = q.filter(Medication.patient == patient)
    return q.all()


def sync_medications(patient, medications_to_keep):
    def log(medication):
        logger.info('Deleting medication id={}'.format(medication.id))

    medications = get_medications(patient)
    delete_list(medications, medications_to_keep, delete_f=log)


def build_medication_id(patient, group, sda_medication):
    return build_id(patient.id, Medication.__tablename__, group.id, sda_medication.external_id)


def convert_medications(patient, sda_medications):
    user = get_import_user()

    medications = list()

    for sda_medication in sda_medications:
        # Ignore RaDaR data
        if sda_medication.entered_at == 'RADAR':
            continue

        code = sda_medication.entering_organization
        source_group = get_group(code)

        if source_group is None:
            logger.error('Ignoring medication due to unknown entering organization code={code}'.format(code=code))
            continue

        medication_id = build_medication_id(patient, source_group, sda_medication)
        medication = get_medication(medication_id)

        if medication is None:
            logger.info('Creating medication id={id}'.format(id=medication_id))
            medication = Medication(id=medication_id)
        else:
            logger.info('Updating medication id={id}'.format(id=medication_id))

        medication.patient = patient
        medication.source_group = source_group
        medication.source_type = 'UKRDC'
        medication.created_user = user
        medication.modified_user = user

        medication.from_date = sda_medication.from_date
        medication.to_date = sda_medication.to_date
        medication.drug_text = sda_medication.order_item_description
        medication.dose_text = sda_medication.dose_uom

        db.session.add(medication)
        medications.append(medication)

    return medications


def import_medications(patient, sda_medications):
    logger.info('Importing medications')

    preload_medications(patient)

    sda_medications = parse_medications(sda_medications)
    sda_medications = unique_medications(sda_medications)
    medications = convert_medications(patient, sda_medications)
    sync_medications(patient, medications)

    logger.info('Imported {n} medication(s)'.format(n=len(medications)))
