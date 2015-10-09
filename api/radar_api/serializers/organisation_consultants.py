from radar_api.serializers.consultant_fields import ConsultantReferenceField
from radar_api.serializers.meta import MetaSerializerMixin
from radar_api.serializers.organisations import OrganisationReferenceField
from radar.models import OrganisationConsultant
from radar.serializers.models import ModelSerializer


class OrganisationConsultantSerializer(MetaSerializerMixin, ModelSerializer):
    organisation = OrganisationReferenceField()
    consultant = ConsultantReferenceField()

    class Meta(object):
        model_class = OrganisationConsultant
        exclude = ['organisation_id', 'consultant_id']
