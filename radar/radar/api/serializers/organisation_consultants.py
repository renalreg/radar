from radar.api.serializers.consultant_fields import ConsultantReferenceField
from radar.api.serializers.meta import MetaSerializerMixin
from radar.api.serializers.organisations import OrganisationReferenceField
from radar.lib.models import OrganisationConsultant
from radar.lib.serializers.models import ModelSerializer


class OrganisationConsultantSerializer(MetaSerializerMixin, ModelSerializer):
    organisation = OrganisationReferenceField()
    consultant = ConsultantReferenceField()

    class Meta(object):
        model_class = OrganisationConsultant
        exclude = ['organisation_id', 'consultant_id']
