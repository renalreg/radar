from radar.lib.database import db
from radar.models import LabGroupDefinition, LabResultDefinition, LabGroupResultDefinition


def create_lab_group_definitions():
    group_definition = LabGroupDefinition(code='TEST', name='Example Test', short_name='Example Test', pre_post=True)
    db.session.add(group_definition)

    result1_definition = LabResultDefinition(code='FOO', name='Foo', short_name='Foo', units='foo')
    db.session.add(result1_definition)

    result2_definition = LabResultDefinition(code='BAR', name='Bar', short_name='Bar', units='bar')
    db.session.add(result2_definition)

    result3_definition = LabResultDefinition(code='BAZ', name='Baz', short_name='Baz', units='baz')
    db.session.add(result3_definition)

    group_result1_definition = LabGroupResultDefinition(lab_group_definition=group_definition, lab_result_definition=result1_definition, weight=1)
    db.session.add(group_result1_definition)

    group_result2_definition = LabGroupResultDefinition(lab_group_definition=group_definition, lab_result_definition=result2_definition, weight=2)
    db.session.add(group_result2_definition)

    group_result3_definition = LabGroupResultDefinition(lab_group_definition=group_definition, lab_result_definition=result3_definition, weight=3)
    db.session.add(group_result3_definition)
