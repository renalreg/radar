from cornflake import fields
from cornflake.sqlalchemy_orm import ModelSerializer
from cornflake.validators import min_, range_

from radar.api.serializers.common import MetaMixin, PatientMixin, StringLookupField
from radar.api.serializers.validators import valid_date_for_patient
from radar.models.pregnancies import (
    DELIVERY_METHODS,
    OUTCOMES,
    PRE_ECLAMPSIA_TYPES,
    Pregnancy,
)
from radar.variants import pick


class BasePregnancySerializer(PatientMixin, MetaMixin, ModelSerializer):
    """Fields shared by every deployment."""

    pregnancy_number = fields.IntegerField(validators=[min_(1)])
    gravidity = fields.IntegerField(required=False, validators=[range_(0, 9)])
    parity1 = fields.IntegerField(required=False, validators=[range_(0, 9)])
    parity2 = fields.IntegerField(required=False, validators=[range_(0, 9)])
    outcome = StringLookupField(OUTCOMES, required=False)
    weight = fields.IntegerField(required=False, validators=[range_(200, 5000)])
    weight_centile = fields.IntegerField(required=False, validators=[range_(20, 90)])
    gestational_age = fields.IntegerField(
        required=False, validators=[range_(20 * 7, 42 * 7, "days")]
    )
    delivery_method = StringLookupField(DELIVERY_METHODS, required=False)
    neonatal_intensive_care = fields.BooleanField(required=False)
    pre_eclampsia = StringLookupField(PRE_ECLAMPSIA_TYPES, required=False)

    class Meta:
        model_class = Pregnancy
        validators = [valid_date_for_patient("date_of_lmp")]


class MainPregnancySerializer(BasePregnancySerializer):
    date_of_lmp = fields.DateField(required=False)
    infant_dob = fields.DateField(required=False)


class InternationalPregnancySerializer(BasePregnancySerializer):
    date_of_lmp = fields.DateField()


PregnancySerializer: (
    type[MainPregnancySerializer] | type[InternationalPregnancySerializer]
) = pick(
    main=MainPregnancySerializer,
    international=InternationalPregnancySerializer,
)
