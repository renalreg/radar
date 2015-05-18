from flask_wtf import Form
from radar.forms import UnitFormMixin, RadarDateField, RadarSelectObjectField, RadarYesNoField
from wtforms.validators import InputRequired, Optional


class TransplantForm(UnitFormMixin, Form):
    transplant_date = RadarDateField(validators=[InputRequired()])
    transplant_type = RadarSelectObjectField(validators=[InputRequired()])
    recurred = RadarYesNoField(validators=[Optional()])
    date_recurred = RadarDateField(validators=[Optional()])
    date_failure = RadarDateField(validators=[Optional()])