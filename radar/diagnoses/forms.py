from flask_wtf import Form
from wtforms import StringField


class DiagnosisForm(Form):
    diagnosis = StringField()