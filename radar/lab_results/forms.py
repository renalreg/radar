from wtforms import Form
from wtforms.validators import Optional

from radar.forms import RadarSelectMultipleField, RadarSelectField


class LabResultTableForm(Form):
    test_item = RadarSelectMultipleField('Columns', validators=[Optional()])


class LabResultGraphForm(Form):
    test_item = RadarSelectField()