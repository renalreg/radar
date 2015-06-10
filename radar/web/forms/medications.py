from flask_wtf import Form
from wtforms import BooleanField, HiddenField
from wtforms.validators import InputRequired, Optional
from wtforms.widgets import HiddenInput

from radar.lib.database import db
from radar.models.medications import MedicationDoseUnit, MedicationFrequency, MedicationRoute
from radar.web.forms.core import RadarDateField, add_empty_object_choice, FacilityFormMixin, RadarSelectObjectField, \
    RadarDecimalField, RadarStringField


class MedicationForm(FacilityFormMixin, Form):
    def __init__(self, obj=None, **kwargs):
        super(MedicationForm, self).__init__(obj=obj, **kwargs)

        self.dose_unit_id.choices = add_empty_object_choice(MedicationDoseUnit.choices(db.session))
        self.frequency_id.choices = add_empty_object_choice(MedicationFrequency.choices(db.session))
        self.route_id.choices = add_empty_object_choice(MedicationRoute.choices(db.session))

        self.updated = (
            obj is not None and
            (
                obj.dose_quantity != self.dose_quantity.data or
                obj.frequency_id != self.frequency_id.data or
                obj.route_id != self.route_id.data
            )
        )

        self.show_update_warning = False

    from_date = RadarDateField(validators=[InputRequired()])
    to_date = RadarDateField(validators=[Optional()])

    name = RadarStringField(validators=[InputRequired()])
    dose_quantity = RadarDecimalField(validators=[InputRequired()])
    dose_unit_id = RadarSelectObjectField('Dose Unit', validators=[InputRequired()])
    frequency_id = RadarSelectObjectField('Frequency', validators=[InputRequired()])
    route_id = RadarSelectObjectField('Route', validators=[InputRequired()])

    shown_update_warning = HiddenField()

    def validate(self):
        if not super(MedicationForm, self).validate():
            return False

        valid = True

        if self.updated and not self.shown_update_warning.data:
            valid = False
            self.show_update_warning = True
            self.shown_update_warning.data = 'y'

        return valid

    def populate_obj(self, obj):
        obj.facility = self.facility_id.obj
        obj.from_date = self.from_date.data
        obj.to_date = self.to_date.data
        obj.name = self.name.data
        obj.dose_quantity = self.dose_quantity.data
        obj.dose_unit = self.dose_unit_id.obj
        obj.frequency = self.frequency_id.obj
        obj.route = self.route_id.obj
