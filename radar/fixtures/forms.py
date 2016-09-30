import json
import os
import pkg_resources

from radar.models.groups import Group, GROUP_TYPE
from radar.models.forms import Form, GroupForm

from radar.fixtures.utils import add

filenames = [
    ('6cit.json', '6CIT'),
    ('anthropometric.json', 'Anthropometric'),
    ('diabetes.json', 'Diabetes'),
    ('diabetic-complications.json', 'Diabetic Complications'),
    ('eq-5d-5l.json', 'EQ-5D-5L'),
    ('hads.json', 'HADS'),
    ('ipos.json', 'IPOS'),
    ('pam.json', 'PAM'),
    ('socio-economic.json', 'Socio-Economic'),
    ('eq-5d-y.json', 'EQ-5D-Y'),
    ('chu9d.json', 'CHU9D'),
]

questionnaires = {
    'NURTURE': set([
        '6CIT', 'CHU9D', 'EQ-5D-5L', 'EQ-5D-Y', 'HADS', 'IPOS', 'PAM',
    ])
}


def create_forms():
    for filename, name in filenames:
        filename = os.path.join('forms', filename)
        f = pkg_resources.resource_stream(__name__, filename)
        data = json.load(f)

        form = Form()
        form.name = name
        form.data = data
        add(form)

    for code, forms in questionnaires.items():
        group = Group.query.filter(Group.code == code, Group.type == GROUP_TYPE.COHORT).one()

        for form in forms:
            form = Form.query.filter(Form.name == form).one()

            group_form = GroupForm()
            group_form.group = group
            group_form.form = form
            add(group_form)
