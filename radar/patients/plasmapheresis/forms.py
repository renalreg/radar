from flask_wtf import Form
from radar.forms import UnitFormMixin, RadarDateField, RadarSelectObjectField
from wtforms import IntegerField
from wtforms.validators import InputRequired, Optional


class PlasmapheresisForm(UnitFormMixin, Form):
    date_started = RadarDateField(validators=[InputRequired()])
    date_stopped = RadarDateField(validators=[Optional()])
    number_of_exchanges = IntegerField(validators=[Optional()])
    response_id = RadarSelectObjectField(validators=[Optional()])