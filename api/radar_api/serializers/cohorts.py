from radar_api.serializers.meta import MetaSerializerMixin
from radar.serializers.fields import ListField, StringField
from radar.serializers.models import ModelSerializer, ReferenceField
from radar.models import Cohort


class TinyCohortSerializer(ModelSerializer):
    class Meta(object):
        model_class = Cohort
        fields = ['id', 'code', 'name', 'short_name']


class CohortSerializer(MetaSerializerMixin, ModelSerializer):
    features = ListField(StringField(), source='sorted_features', read_only=True)

    class Meta(object):
        model_class = Cohort


class CohortReferenceField(ReferenceField):
    model_class = Cohort
    serializer_class = CohortSerializer


class TinyCohortReferenceField(ReferenceField):
    model_class = Cohort
    serializer_class = TinyCohortSerializer


class CohortSerializerMixin(object):
    cohort = CohortReferenceField()

    def get_model_exclude(self):
        attrs = super(CohortSerializerMixin, self).get_model_exclude()
        attrs.add('cohort_id')
        return attrs
