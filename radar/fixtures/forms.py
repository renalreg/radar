import json
import os
import pkg_resources

from radar.models.forms import Form
from radar.fixtures.utils import add

filenames = [
    ('6cit.json', '6CIT'),
    ('anthropometrics.json', 'Anthropometric'),
    ('family-history.json', 'Family History'),
    ('diabetic-complications.json', 'Diabetic Complications'),
    ('eq-5d-5l.json', 'EQ-5D-5L'),
    ('hads.json', 'HADS'),
    ('ipos.json', 'IPOS'),
    ('pam.json', 'PAM'),
    ('samples.json', 'Samples'),
    ('socio-economic.json', 'Socio-Economic'),
    ('eq-5d-y.json', 'EQ-5D-Y'),
    ('chu9d.json', 'CHU9D'),
]


def create_forms():
    for filename, name in filenames:
        slug = os.path.splitext(filename)[0]

        filename = os.path.join('forms', filename)
        f = pkg_resources.resource_stream(__name__, filename)
        data = json.load(f)

        form = Form()
        form.name = name
        form.slug = slug
        form.data = data
        add(form)
