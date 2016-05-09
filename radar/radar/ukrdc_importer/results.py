import logging
from functools import partial

from radar.models.results import Result, Observation
from radar.database import db
from radar.groups import is_radar_group

from radar_ukrdc_importer.utils import (
    load_validator,
    validate_list,
    unique_list,
    parse_datetime_path,
    delete_list,
    build_id,
    get_path,
    get_import_user,
    get_group
)


logger = logging.getLogger(__name__)


class SDALabResultItem(object):
    def __init__(self, data, parent=None):
        self.data = data
        self.parent = parent

    @property
    def observation_time(self):
        return self.data.get('observation_time')

    @property
    def test_item_code(self):
        return self.data['test_item_code']['code']

    @property
    def result_value(self):
        return self.data['result_value']


class SDALabOrder(object):
    def __init__(self, data):
        self.data = data

        sda_lab_result_item = partial(SDALabResultItem, parent=self)
        self.results = map(sda_lab_result_item, self.data['result']['result_items'])

    @property
    def external_id(self):
        return self.data['external_id']

    @property
    def from_time(self):
        return self.data.get('from_time')

    @property
    def entering_organization(self):
        return get_path(self.data, 'entering_organization', 'code')


def parse_results(sda_lab_orders):
    def log(index, sda_lab_order, error):
        logger.error('Ignoring invalid lab order index={index}'.format(index=index))

    validator = load_validator('lab_order.json')
    sda_lab_orders = validate_list(sda_lab_orders, validator, invalid_f=log)

    for sda_lab_order in sda_lab_orders:
        parse_datetime_path(sda_lab_order, 'from_time')

        for sda_lab_result_item in sda_lab_order['result']['result_items']:
            parse_datetime_path(sda_lab_order, 'observation_time')

    sda_lab_orders = map(SDALabOrder, sda_lab_orders)

    return sda_lab_orders


def unique_results(sda_lab_orders):
    def key(sda_lab_order):
        return sda_lab_order.external_id

    def log(sda_lab_order):
        external_id = sda_lab_order.external_id
        logger.error('Ignoring duplicate lab order external_id={external_id}'.format(external_id=external_id))

    sda_lab_orders = unique_list(sda_lab_orders, key_f=key, duplicate_f=log)

    return sda_lab_orders


def preload_results(patient):
    """Preload results so get(id) can use the identity map rather than querying the database"""
    get_results(patient)


def get_result(result_id):
    return Result.query.get(result_id)


def get_results(patient, min_date=None):
    q = Result.query
    q = q.filter(Result.source_type == 'UKRDC')
    q = q.filter(Result.patient == patient)

    if min_date is not None:
        q = q.filter(Result.date >= min_date)

    return q.all()


def get_observation(code):
    return Observation.query.filter(Observation.pv_code == code).first()


def sync_results(patient, results_to_keep):
    """Deletes results on or after the earliest date in the input data"""

    def log(result):
        logger.info('Deleting result id={}'.format(result.id))

    # Need at least one result to work out which results to delete
    if len(results_to_keep) == 0:
        return

    # Find earliest date from input data
    min_date = min(results_to_keep, key=lambda x: x.date).date

    # Get results on or after the min date
    results = get_results(patient, min_date=min_date)

    delete_list(results, results_to_keep, delete_f=log)


def build_result_id(patient, group, sda_lab_result_item):
    return build_id(
        patient.id,
        Result.__tablename__,
        group.id,
        sda_lab_result_item.parent.external_id,
        sda_lab_result_item.test_item_code
    )


def convert_results(patient, sda_lab_orders):
    user = get_import_user()

    results = list()

    for sda_lab_order in sda_lab_orders:
        code = sda_lab_order.entering_organization
        source_group = get_group(code)

        if source_group is None:
            logger.error('Ignoring lab order due to unknown entering organization code={code}'.format(code=code))
            continue

        # Ignore RaDaR data
        if is_radar_group(source_group):
            continue

        for sda_lab_result_item in sda_lab_order.results:
            test_item_code = sda_lab_result_item.test_item_code
            observation = get_observation(test_item_code)

            if observation is None:
                logger.error('Ignoring lab result due to unknown test item code={code}'.format(code=test_item_code))
                continue

            dt = sda_lab_result_item.observation_time or sda_lab_order.from_time

            if dt is None:
                logger.error('Ignoring lab result due to missing date')
                continue

            result_id = build_result_id(patient, source_group, sda_lab_result_item)
            result = get_result(result_id)

            if result is None:
                logger.info('Creating result id={id}'.format(id=result_id))
                result = Result(id=result_id)
            else:
                logger.info('Updating result id={id}'.format(id=result_id))

            result.patient = patient
            result.source_group = source_group
            result.source_type = 'UKRDC'
            result.created_user = user
            result.modified_user = user

            result.date = dt
            result.observation = observation
            result.value = sda_lab_result_item.result_value

            db.session.add(result)
            results.append(result)

    return results


def import_results(patient, sda_lab_orders):
    logger.info('Importing results')

    preload_results(patient)

    sda_lab_orders = parse_results(sda_lab_orders)
    sda_lab_orders = unique_results(sda_lab_orders)
    results = convert_results(patient, sda_lab_orders)
    sync_results(patient, results)

    logger.info('Imported {n} results(s)'.format(n=len(results)))
