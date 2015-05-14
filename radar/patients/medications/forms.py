from flask_wtf import Form
from radar.database import db
from radar.patients.medications.models import MedicationDoseUnit, MedicationFrequency, MedicationRoute
from wtforms import StringField, DecimalField
from wtforms.validators import InputRequired, Optional

from radar.forms import RadarDateField, RadarSelectField, add_empty_choice, UnitFormMixin


class MedicationForm(UnitFormMixin, Form):
    def __init__(self, *args, **kwargs):
        super(MedicationForm, self).__init__(*args, **kwargs)

        self.dose_unit_id.choices = add_empty_choice(MedicationDoseUnit.choices(db.session))
        self.frequency_id.choices = add_empty_choice(MedicationFrequency.choices(db.session))
        self.route_id.choices = add_empty_choice(MedicationRoute.choices(db.session))

    from_date = RadarDateField(validators=[InputRequired()])
    to_date = RadarDateField(validators=[Optional()])

    name = StringField(validators=[InputRequired()])
    dose_quantity = DecimalField(validators=[InputRequired()])
    dose_unit_id = RadarSelectField('Dose Unit', validators=[InputRequired()])
    frequency_id = RadarSelectField('Frequency', validators=[InputRequired()])
    route_id = RadarSelectField('Route', validators=[InputRequired()])