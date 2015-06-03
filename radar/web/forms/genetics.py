from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import Optional, InputRequired
from wtforms.widgets import TextArea

from radar.web.forms.core import RadarYesNoField, RadarDateField


class GeneticsForm(Form):
    sample_sent = RadarYesNoField("Has a sample been sent for Genetic analysis?", validators=[InputRequired()])
    sample_sent_date = RadarDateField("Date Sent", validators=[Optional()])
    laboratory = StringField("Laboratory where test sent / done", validators=[Optional()])
    laboratory_reference_number = StringField("Laboratory Reference No.", validators=[Optional()])
    results = StringField(widget=TextArea(), validators=[Optional()])
