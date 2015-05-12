from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import InputRequired

from radar.forms import RadarDateField


class MedicationForm(Form):
    from_date = RadarDateField(validators=[InputRequired()])
    to_date = RadarDateField(validators=[InputRequired()])
    name = StringField(validators=[InputRequired()])

    def populate_obj(self, obj):
        obj.from_date = self.from_date.data
        obj.to_date = self.to_date.data
        obj.name = self.name.data