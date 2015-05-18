from flask_wtf import Form
from radar.database import db
from radar.forms import RadarDateField, UnitFormMixin, add_empty_object_choice, RadarSelectObjectField
from radar.patients.dialysis.models import DialysisType
from radar.utils import optional_int
from wtforms.validators import InputRequired, Optional


class DialysisForm(UnitFormMixin, Form):
    def __init__(self, *args, **kwargs):
        super(DialysisForm, self).__init__(*args, **kwargs)

        self.dialysis_type_id.choices = add_empty_object_choice(DialysisType.choices(db.session))

    from_date = RadarDateField(validators=[InputRequired()])
    to_date = RadarDateField(validators=[Optional()])
    dialysis_type_id = RadarSelectObjectField('Dialysis Type', validators=[InputRequired()], coerce=optional_int)