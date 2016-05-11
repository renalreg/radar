import logging

from radar.models.patient_aliases import PatientAlias
from radar.database import db

from radar.ukrdc_importer.serializers import NameSerializer
from radar.ukrdc_importer.utils import (
    validate_list,
    unique_list,
    delete_list,
    build_id,
    get_import_group,
    get_import_user
)


logger = logging.getLogger(__name__)


class SDAName(object):
    def __init__(self, data):
        self.data = data

    @property
    def given_name(self):
        return self.data['given_name']

    @property
    def family_name(self):
        return self.data['family_name']


def parse_aliases(sda_names):
    def log(index, sda_name, e):
        logger.error('Ignoring invalid alias index={index}, errors={errors}'.format(index=index, errors=e.flatten()))

    serializer = NameSerializer()
    sda_names = validate_list(sda_names, serializer, invalid_f=log)
    sda_names = map(SDAName, sda_names)

    return sda_names


def unique_aliases(sda_names):
    def key(sda_name):
        return (sda_name.given_name, sda_name.family_name)

    def log(sda_name):
        logger.error('Ignoring duplicate alias')

    sda_names = unique_list(sda_names, key_f=key, duplicate_f=log)

    return sda_names


def get_alias(alias_id):
    return PatientAlias.query.get(alias_id)


def get_aliases(patient):
    q = PatientAlias.query
    q = q.filter(PatientAlias.source_type == 'UKRDC')
    q = q.filter(PatientAlias.patient == patient)
    return q.all()


def sync_aliases(patient, alises_to_keep):
    def log(alias):
        logger.info('Deleting alias id={}'.format(alias.id))

    aliases = get_aliases(patient)
    delete_list(aliases, alises_to_keep, delete_f=log)


def build_alias_id(patient, sda_name):
    return build_id(patient.id, PatientAlias.__tablename__, sda_name.given_name, sda_name.family_name)


def convert_aliases(patient, sda_names):
    source_group = get_import_group()
    user = get_import_user()

    aliases = list()

    for sda_name in sda_names:
        alias_id = build_alias_id(patient, sda_name)
        alias = get_alias(alias_id)

        if alias is None:
            logger.info('Creating alias id={id}'.format(id=alias_id))
            alias = PatientAlias(id=alias_id)
        else:
            logger.info('Updating alias id={id}'.format(id=alias_id))

        alias.patient = patient
        alias.source_group = source_group
        alias.source_type = 'UKRDC'
        alias.created_user = user
        alias.modified_user = user

        alias.first_name = sda_name.given_name
        alias.last_name = sda_name.family_name

        db.session.add(alias)
        aliases.append(alias)

    return aliases


def import_aliases(patient, sda_names):
    logger.info('Importing aliases')

    sda_names = parse_aliases(sda_names)
    sda_names = unique_aliases(sda_names)
    aliases = convert_aliases(patient, sda_names)
    sync_aliases(patient, aliases)

    logger.info('Imported {n} alias(es)'.format(n=len(aliases)))
