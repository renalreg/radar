from flask_wtf import Form
from wtforms import StringField, DecimalField
from wtforms.validators import InputRequired, Optional

from radar.lib.database import db
from radar.models.medications import MedicationDoseUnit, MedicationFrequency, MedicationRoute
from radar.lib.forms.common import RadarDateField, add_empty_object_choice, UnitFormMixin, RadarSelectObjectField


class MedicationForm(UnitFormMixin, Form):
    def __init__(self, *args, **kwargs):
        super(MedicationForm, self).__init__(*args, **kwargs)

        self.dose_unit_id.choices = add_empty_object_choice(MedicationDoseUnit.choices(db.session))
        self.frequency_id.choices = add_empty_object_choice(MedicationFrequency.choices(db.session))
        self.route_id.choices = add_empty_object_choice(MedicationRoute.choices(db.session))

    from_date = RadarDateField(validators=[InputRequired()])
    to_date = RadarDateField(validators=[Optional()])

    name = StringField(validators=[InputRequired()])
    dose_quantity = DecimalField(validators=[InputRequired()])
    dose_unit_id = RadarSelectObjectField('Dose Unit', validators=[InputRequired()])
    frequency_id = RadarSelectObjectField('Frequency', validators=[InputRequired()])
    route_id = RadarSelectObjectField('Route', validators=[InputRequired()])