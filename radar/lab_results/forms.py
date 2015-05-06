from wtforms import Form

from radar.forms import RadarSelectMultipleField


class LabResultTableForm(Form):
    item = RadarSelectMultipleField('Columns')