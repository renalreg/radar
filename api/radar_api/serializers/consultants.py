from radar_api.serializers.organisations import OrganisationReferenceField
from radar_api.serializers.meta import MetaSerializerMixin
from radar.serializers.fields import ListField
from radar.serializers.models import ModelSerializer
from radar.models.consultants import Consultant
from radar.models.organisations import OrganisationConsultant


class ConsultantSerializer(MetaSerializerMixin, ModelSerializer):
    organisations = ListField(field=OrganisationReferenceField())

    class Meta(object):
        model_class = Consultant

    def create_organisation_consultant(self, deserialized_data):
        organisation_consultant = OrganisationConsultant()
        organisation_consultant.organisation = deserialized_data
        return organisation_consultant

    def update(self, obj, deserialized_data):
        for attr, value in deserialized_data.items():
            if attr == 'organisations':
                obj.organisation_consultants = []

                for x in value:
                    organisation_consultant = self.create_organisation_consultant(x)
                    obj.organisation_consultants.append(organisation_consultant)
            elif hasattr(obj, attr):
                setattr(obj, attr, value)

        return obj
