import json
import os

from radar.models.groups import Group, GROUP_TYPE
from radar.models.forms import Form, GroupForm

from radar_fixtures.utils import add

here = os.path.dirname(os.path.abspath(__file__))
form_dir = os.path.abspath(os.path.join(here, '../../../extra/forms'))
print form_dir

filenames = [
    ('6cit.json', '6CIT'),
    ('anthropometric.json', 'Anthropometric'),
    ('diabetes.json', 'Diabetes'),
    ('diabetic-complications.json', 'Diabetic Complications'),
    ('eq-5d-5l.json', 'EQ5D'),
    ('hads.json', 'HADS'),
    ('ipos.json', 'IPOS'),
    ('pam.json', 'PAM'),
    ('socio-economic.json', 'Socio-Economic'),
]

questionnaires = {
    'NURTURE': set([
        '6CIT', 'EQ5D', 'HADS', 'IPOS', 'PAM',
    ])
}


def create_forms():
    for filename, name in filenames:
        filename = os.path.join(form_dir, filename)
        data = json.load(open(filename))

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
