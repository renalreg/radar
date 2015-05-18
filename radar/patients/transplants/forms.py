from flask_wtf import Form
from radar.database import db
from radar.forms import UnitFormMixin, RadarDateField, RadarSelectObjectField, RadarYesNoField, add_empty_object_choice
from radar.patients.transplants.models import TransplantType
from radar.utils import optional_int
from wtforms.validators import InputRequired, Optional


class TransplantForm(UnitFormMixin, Form):
    def __init__(self, *args, **kwargs):
        super(TransplantForm, self).__init__(*args, **kwargs)

        self.transplant_type_id.choices = add_empty_object_choice(TransplantType.choices(db.session))

    transplant_date = RadarDateField(validators=[InputRequired()])
    transplant_type_id = RadarSelectObjectField('Transplant Type', validators=[InputRequired()], coerce=optional_int)
    reoccurred = RadarYesNoField(validators=[Optional()])
    date_reoccurred = RadarDateField(validators=[Optional()])
    date_failed = RadarDateField(validators=[Optional()])