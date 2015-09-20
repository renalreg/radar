from radar.api.serializers.meta import MetaSerializerMixin
from radar.lib.serializers.fields import ListField, StringField
from radar.lib.serializers.models import ModelSerializer, ReferenceField
from radar.lib.models import CohortFeature, Cohort


class CohortSerializer(MetaSerializerMixin, ModelSerializer):
    features = ListField(StringField(), source='sorted_features')

    class Meta(object):
        model_class = Cohort


class CohortReferenceField(ReferenceField):
    model_class = Cohort
    serializer_class = CohortSerializer


class CohortSerializerMixin(object):
    cohort = CohortReferenceField()

    def get_model_exclude(self):
        attrs = super(CohortSerializerMixin, self).get_model_exclude()
        attrs.add('cohort_id')
        return attrs
