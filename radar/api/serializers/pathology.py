from cornflake import fields
from cornflake.sqlalchemy_orm import ModelSerializer
from cornflake.validators import max_length, none_if_blank, optional, url

from radar.api.serializers.common import (
    MetaMixin,
    PatientMixin,
    SourceMixin,
    StringLookupField,
)
from radar.api.serializers.validators import valid_date_for_patient
from radar.models.pathology import (
    Pathology,
    PATHOLOGY_KIDNEY_SIDES,
    PATHOLOGY_KIDNEY_TYPES,
)
from radar.variants import pick


class BasePathologySerializer(PatientMixin, SourceMixin, MetaMixin, ModelSerializer):
    """Fields shared by every deployment."""

    date = fields.DateField()
    kidney_type = StringLookupField(PATHOLOGY_KIDNEY_TYPES, required=False)
    kidney_side = StringLookupField(PATHOLOGY_KIDNEY_SIDES, required=False)
    reference_number = fields.StringField(
        required=False, validators=[none_if_blank(), optional(), max_length(100)]
    )
    image_url = fields.StringField(
        required=False, validators=[none_if_blank(), optional(), url()]
    )
    histological_summary = fields.StringField(
        required=False, validators=[none_if_blank(), optional(), max_length(10000)]
    )
    em_findings = fields.StringField(
        required=False, validators=[none_if_blank(), optional(), max_length(10000)]
    )

    class Meta:
        model_class = Pathology
        validators = [valid_date_for_patient("date")]


class MainPathologySerializer(BasePathologySerializer):
    report_cleaned = fields.DateField(required=False)


class InternationalPathologySerializer(BasePathologySerializer):
    pass


PathologySerializer: (
    type[MainPathologySerializer] | type[InternationalPathologySerializer]
) = pick(
    main=MainPathologySerializer,
    international=InternationalPathologySerializer,
)
