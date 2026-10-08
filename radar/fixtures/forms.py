import json
import os
from importlib.resources import files

from radar.fixtures.utils import add
from radar.models.forms import Form

filenames = [
    ("6cit.json", "6CIT"),
    ("anthropometrics.json", "Anthropometrics"),
    ("family-history.json", "Family History"),
    ("diabetic-complications.json", "Diabetic Complications"),
    ("eq-5d-5l.json", "EQ-5D-5L"),
    ("hads.json", "HADS"),
    ("ipos.json", "IPOS"),
    ("pam.json", "PAM"),
    ("samples.json", "Samples"),
    ("socio-economic.json", "Socio-Economic"),
    ("eq-5d-y.json", "EQ-5D-Y"),
    ("chu9d.json", "CHU9D"),
]

FORMS_DIR = files("radar.fixtures") / "forms"


def create_forms():
    for filename, name in filenames:
        slug = os.path.splitext(filename)[0]

        data = json.loads((FORMS_DIR / filename).read_text(encoding="utf-8"))

        form = Form()
        form.name = name
        form.slug = slug
        form.data = data
        add(form)
