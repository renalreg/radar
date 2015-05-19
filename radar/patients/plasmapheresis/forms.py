from flask_wtf import Form
from radar.database import db
from radar.forms import UnitFormMixin, RadarDateField, RadarSelectObjectField, add_empty_object_choice
from radar.patients.plasmapheresis.models import PlasmapheresisResponse
from radar.utils import optional_int
from wtforms import IntegerField
from wtforms.validators import InputRequired, Optional


class PlasmapheresisForm(UnitFormMixin, Form):
    def __init__(self, *args, **kwargs):
        super(PlasmapheresisForm, self).__init__(*args, **kwargs)

        self.response_id.choices = add_empty_object_choice(PlasmapheresisResponse.choices(db.session))

    from_date = RadarDateField(validators=[InputRequired()])
    to_date = RadarDateField(validators=[Optional()])
    no_of_exchanges = IntegerField('No. of Exchanges', validators=[Optional()])
    response_id = RadarSelectObjectField('Response', validators=[Optional()], coerce=optional_int)