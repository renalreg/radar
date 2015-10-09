from xml.etree.ElementTree import Element, SubElement

from radar.lib.sda.models import SDALabOrder, SDABundle
from radar.lib.utils import get_path_as_datetime


def patient_to_xml(patient):
    container_node = Element('Container')

    lab_orders_node = SubElement(container_node, 'LabOrders')

    lab_orders = SDALabOrder.query\
        .join(SDALabOrder.sda_bundle)\
        .filter(SDABundle.patient == patient)\
        .all()

    for lab_order in lab_orders:
        lab_orders_node.append(lab_order_to_xml(lab_order))

    return container_node


def lab_order_to_xml(lab_order):
    node = Element('LabOrder')

    from_time = get_path_as_datetime(lab_order.data, ['from_time'])

    if from_time is not None:
        from_time_node = SubElement(node, 'FromTime')
        from_time_node.text = from_time.isoformat()

    return node
