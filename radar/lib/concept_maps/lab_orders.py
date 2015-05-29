from collections import defaultdict

from radar.lib.concepts.lab_orders import LabOrderConcept


class LabOrderConceptMap(object):
    def __init__(self, lab_order):
        self.lab_order = lab_order
        self.lab_order_concept = LabOrderConcept(lab_order)

    def validate(self):
        valid = True
        errors = defaultdict(list)

        if not self.lab_order_concept.validate():
            valid = False

        return valid, errors

    def to_sda(self, sda_bundle):
        self.lab_order_concept.to_sda(sda_bundle)