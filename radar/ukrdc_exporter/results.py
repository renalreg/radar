from sqlalchemy import null

from radar.models.results import Result, Observation
from radar.models.source_types import SOURCE_TYPE_MANUAL


def export_lab_orders(sda_container, patient, group):
    q = Result.query
    q = q.filter(Result.patient == patient)
    q = q.filter(Result.source_group == group)
    q = q.filter(Result.source_type == SOURCE_TYPE_MANUAL)
    q = q.join(Result.observation)
    q = q.filter(Observation.pv_code != null())
    results = q.all()

    if not results:
        return

    sda_lab_orders = sda_container.setdefault('lab_orders', list())

    for result in results:
        sda_lab_order = {
            'external_id': str(result.id),
            'order_item': {
                'sda_coding_standard': 'PV',
                'code': result.observation.pv_code,
                'description': result.observation.pv_code
            },
            'result': {
                'result_time': result.date,
                'result_items': [
                    {
                        'observation_time': result.date,
                        'test_item_code': {
                            'sda_coding_standard': 'PV',
                            'code': result.observation.pv_code,
                            'description': result.observation.pv_code
                        },
                        'result_value': str(result.value)
                    }
                ]
            },
            'entering_organization': {
                'code': result.source_group.code,
                'description': result.source_group.name
            },
            'entered_at': {
                'code': 'RADAR',
                'description': 'RaDaR'
            }
        }

        sda_lab_orders.append(sda_lab_order)
