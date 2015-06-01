from flask_wtf import Form
from wtforms import StringField, DecimalField
from wtforms.validators import InputRequired, Optional

from radar.lib.database import db
from radar.models.medications import MedicationDoseUnit, MedicationFrequency, MedicationRoute
from radar.web.forms.core import RadarDateField, add_empty_object_choice, FacilityFormMixin, RadarSelectObjectField


class MedicationForm(FacilityFormMixin, Form):
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

    def populate_obj(self, obj):
        obj.facility = self.facility_id.obj
        obj.from_date = self.from_date.data
        obj.to_date = self.to_date.data
        obj.name = self.name.data
        obj.dose_quantity = self.dose_quantity.data
        obj.dose_unit = self.dose_unit_id.obj
        obj.frequency = self.frequency_id.obj
        obj.route = self.route_id.obj