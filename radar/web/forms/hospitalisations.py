from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import InputRequired, Optional

from radar.web.forms.core import FacilityFormMixin, RadarDateField


class HospitalisationForm(FacilityFormMixin, Form):
    date_of_admission = RadarDateField('Date of Admission', validators=[InputRequired()])
    date_of_discharge = RadarDateField('Date of Discharge', validators=[Optional()])
    reason_for_admission = StringField('Reason for Admission', validators=[InputRequired()])
    comments = StringField('Comments', validators=[Optional()])

    def populate_obj(self, obj):
        obj.facility = self.facility_id.obj
        obj.date_of_admission = self.date_of_admission.data
        obj.date_of_discharge = self.date_of_discharge.data
        obj.reason_for_admission = self.reason_for_admission.data
        obj.comments = self.comments.data
