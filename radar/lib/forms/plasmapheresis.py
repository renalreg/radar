from flask_wtf import Form
from wtforms import IntegerField
from wtforms.validators import InputRequired, Optional

from radar.lib.database import db
from radar.lib.forms.common import FacilityFormMixin, RadarDateField, RadarSelectObjectField, add_empty_object_choice
from radar.models.plasmapheresis import PlasmapheresisResponse
from radar.lib.utils import optional_int


class PlasmapheresisForm(FacilityFormMixin, Form):
    def __init__(self, *args, **kwargs):
        super(PlasmapheresisForm, self).__init__(*args, **kwargs)

        self.response_id.choices = add_empty_object_choice(PlasmapheresisResponse.choices(db.session))

    from_date = RadarDateField(validators=[InputRequired()])
    to_date = RadarDateField(validators=[Optional()])
    no_of_exchanges = IntegerField('No. of Exchanges', validators=[Optional()])
    response_id = RadarSelectObjectField('Response', validators=[Optional()], coerce=optional_int)

    def populate_obj(self, obj):
        obj.facility = self.facility_id.obj
        obj.from_date = self.from_date.data
        obj.to_date = self.to_date.data
        obj.no_of_exchanges = self.no_of_exchanges.data
        obj.response = self.response_id.obj