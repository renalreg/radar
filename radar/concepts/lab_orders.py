from radar.concepts.core import Concept
from radar.sda.models import SDALabOrder, SDALabResult


class LabOrderConcept(Concept):
    def __init__(self, lab_order):
        super(LabOrderConcept, self).__init__()

        self.lab_order = lab_order

    def to_sda(self, sda_bundle):
        sda_lab_order = SDALabOrder()

        data = {}
        sda_lab_order.data = data

        for lab_result in self.lab_order.lab_results:
            sda_lab_result = SDALabResult()

            lab_result_definition = lab_result.lab_result_definition

            data = {
                'test_item_code': {
                    'sda_coding_standard': 'RADAR',  # TODO
                    'code': lab_result_definition.code,
                    'description': lab_result_definition.description,
                },
                'result_value': lab_result.value
            }

            if lab_result.units is not None:
                data['result_value_units'] = lab_result.units

            sda_lab_result.data = data

            sda_lab_order.results.append(sda_lab_result)

        sda_bundle.sda_lab_orders.append(sda_lab_order)