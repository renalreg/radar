import logging
from functools import partial

from sqlalchemy import and_, or_

from radar.database import db
from radar.models.results import Result, Observation
from radar.ukrdc_importer.serializers import LabOrderSerializer
from radar.ukrdc_importer.utils import (
    validate_list,
    unique_list,
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

    @property
    def entered_at(self):
        return get_path(self.data, 'entered_at', 'code')


def parse_results(sda_lab_orders):
    def log(index, sda_lab_order, e):
        logger.error('Ignoring invalid lab order index={index}, errors={errors}'.format(index=index, errors=e.flatten()))

    serializer = LabOrderSerializer()
    sda_lab_orders = validate_list(sda_lab_orders, serializer, invalid_f=log)
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


def get_results(patient):
    q = Result.query
    q = q.filter(Result.source_type == 'UKRDC')
    q = q.filter(Result.patient == patient)
    return q.all()


def get_observation(code):
    return Observation.query.filter(Observation.pv_code == code).first()


def find_earliest_observations(results):
    min_dates = {}

    # Find the earliest date for each observation
    for result in results:
        min_date = min_dates.get(result.observation)

        # First time this observation has been seen or an earlier result found
        if min_date is None or result.date < min_date:
            min_dates[result.observation] = result.date

    return min_dates


def sync_results(patient, results_to_keep):
    """Deletes results on or after the earliest date in the input data"""

    # No results in the file, nothing to do
    # This prevents all of the patient's previously imported results being deleted
    if len(results_to_keep) == 0:
        return

    def log(result):
        logger.info('Deleting result id={}'.format(result.id))

    # Find the earliest date for each observation
    min_dates = find_earliest_observations(results_to_keep)

    # Find results that are after the min date for each observation
    clauses = [
        and_(Result.observation == observation, Result.date >= min_date)
        for observation, min_date in min_dates.items()
    ]

    # Fetch previously imported results that we expected to see in this file
    q = Result.query
    q = q.filter(Result.source_type == 'UKRDC')
    q = q.filter(Result.patient == patient)
    q = q.filter(or_(*clauses))
    results = q.all()

    delete_list(results, results_to_keep, delete_f=log)


def build_result_id(patient, group, sda_lab_result_item):
    # The external ID is not enough to identify each result as each lab order may contain many results
    # Currently the lab orders we are receiving only contain one result (may change)
    # The test item code is used along with the external ID to uniquely identify each result
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
        # Ignore RaDaR data
        if sda_lab_order.entered_at == 'RADAR':
            continue

        code = sda_lab_order.entering_organization
        source_group = get_group(code)

        if source_group is None:
            logger.error('Ignoring lab order due to unknown entering organization code={code}'.format(code=code))
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

    # Preload results so calls to get() can use the cache rather than querying the database
    preload_results(patient)

    sda_lab_orders = parse_results(sda_lab_orders)
    sda_lab_orders = unique_results(sda_lab_orders)
    results = convert_results(patient, sda_lab_orders)
    sync_results(patient, results)

    logger.info('Imported {n} results(s)'.format(n=len(results)))
