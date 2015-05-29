from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import InputRequired, Optional

from radar.lib.forms.common import UnitFormMixin, RadarDateField


class HospitalisationForm(UnitFormMixin, Form):
    date_of_admission = RadarDateField('Date of Admission', validators=[InputRequired()])
    date_of_discharge = RadarDateField('Date of Discharge', validators=[InputRequired()])
    reason_for_admission = StringField('Reason for Admission', validators=[InputRequired()])
    comments = StringField('Comments', validators=[Optional()])