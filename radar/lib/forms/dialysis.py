from flask_wtf import Form
from wtforms.validators import InputRequired, Optional

from radar.lib.database import db
from radar.lib.forms.common import RadarDateField, UnitFormMixin, add_empty_object_choice, RadarSelectObjectField
from radar.models.dialysis import DialysisType
from radar.lib.utils import optional_int


class DialysisForm(UnitFormMixin, Form):
    def __init__(self, *args, **kwargs):
        super(DialysisForm, self).__init__(*args, **kwargs)

        self.dialysis_type_id.choices = add_empty_object_choice(DialysisType.choices(db.session))

    from_date = RadarDateField(validators=[InputRequired()])
    to_date = RadarDateField(validators=[Optional()])
    dialysis_type_id = RadarSelectObjectField('Dialysis Type', validators=[InputRequired()], coerce=optional_int)