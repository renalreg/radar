from wtforms import Form
from wtforms.validators import Optional

from radar.forms import RadarSelectMultipleField


class LabResultTableForm(Form):
    item = RadarSelectMultipleField('Columns', validators=[Optional()])