from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import Optional
from wtforms.widgets import TextArea

from radar.lib.forms.common import RadarYesNoField, RadarDateField


class GeneticsForm(Form):
    sample_sent = RadarYesNoField("Has a sample been sent for Genetic analysis?", default=False)
    sample_sent_date = RadarDateField("Date Sent", validators=[Optional()])
    laboratory = StringField("Laboratory where test sent / done", validators=[Optional()])
    laboratory_reference_number = StringField("Laboratory Reference No.", validators=[Optional()])
    results = StringField(widget=TextArea(), validators=[Optional()])

    def validate(self):
        if not super(GeneticsForm, self).validate():
            return False

        valid = True

        if self.sample_sent.data:
            if self.sample_sent_date.data is None:
                valid = False
                self.sample_sent_date.errors.append('Please enter a date.')

        return valid