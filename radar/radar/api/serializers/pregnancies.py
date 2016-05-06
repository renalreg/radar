from cornflake.sqlalchemy_orm import ModelSerializer
from cornflake import fields
from cornflake.validators import range_, min_

from radar.api.serializers.common import PatientMixin, MetaMixin
from radar.models.plasmapheresis import Pregnancy, OUTCOMES, DELIVERY_METHODS, PRE_ECLAMPSIA_TYPES
from radar.api.serializers.validators import valid_date_for_patient


class PregnancySerializer(PatientMixin, MetaMixin, ModelSerializer):
    pregnancy_number = fields.IntegerField(validators=[min_(1)])
    date_of_lmp = fields.DateField()
    gravidity = fields.IntegerField(required=False, validators=[range_(0, 9)])
    parity_1 = fields.IntegerField(required=False, validators=[range_(0, 9)])
    parity_2 = fields.IntegerField(required=False, validators=[range_(0, 9)])
    outcome = fields.StringLookupField(OUTCOMES, required=False)
    weight = fields.IntegerField(required=False, validators=[range_(200, 5000)])
    weight_centile = fields.IntegerField(required=False, validators=[range_(20, 90)])
    gestational_age = fields.IntegerField(required=False, validators=[range_(20 * 7, 42 * 7, 'days')])
    delivery_method = fields.StringLookupField(DELIVERY_METHODS, required=False)
    neonatal_intensive_care = fields.BooleanField(required=False)
    pre_eclampsia = fields.StringField(PRE_ECLAMPSIA_TYPES, required=False)

    class Meta(object):
        model_class = Pregnancy
        validators = [valid_date_for_patient('date_of_lmp')]
