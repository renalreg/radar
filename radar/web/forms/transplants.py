from flask_wtf import Form
from wtforms.validators import InputRequired, Optional

from radar.lib.database import db
from radar.web.forms.core import FacilityFormMixin, RadarDateField, RadarSelectObjectField, RadarYesNoField, add_empty_object_choice
from radar.models.transplants import TransplantType
from radar.lib.utils import optional_int


class TransplantForm(FacilityFormMixin, Form):
    def __init__(self, *args, **kwargs):
        super(TransplantForm, self).__init__(*args, **kwargs)

        self.transplant_type_id.choices = add_empty_object_choice(TransplantType.choices(db.session))

    transplant_date = RadarDateField(validators=[InputRequired()])
    transplant_type_id = RadarSelectObjectField('Transplant Type', validators=[InputRequired()], coerce=optional_int)
    recurred = RadarYesNoField(validators=[Optional()])
    date_recurred = RadarDateField(validators=[Optional()])
    date_failed = RadarDateField(validators=[Optional()])

    def populate_obj(self, obj):
        obj.facility = self.facility_id.obj
        obj.transplant_date = self.transplant_date.data
        obj.transplant_type = self.transplant_type_id.obj
        obj.recurred = self.recurred.data
        obj.date_curred = self.date_recurred.data
        obj.date_failed = self.date_failed.data

        if hasattr(self, 'apples'):
            obj.apples = self.apples.data
