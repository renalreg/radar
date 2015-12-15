from radar_api.serializers.organisations import OrganisationReferenceField
from radar_api.serializers.meta import MetaSerializerMixin
from radar.serializers.fields import ListField
from radar.serializers.models import ModelSerializer
from radar.models.consultants import Consultant
from radar.models.organisations import OrganisationConsultant
from radar.database import db


class OrganisationConsultantSerializer(MetaSerializerMixin, ModelSerializer):
    organisation = OrganisationReferenceField()

    class Meta(object):
        model_class = OrganisationConsultant
        exclude = ['id', 'consultant_id']


class ConsultantSerializer(MetaSerializerMixin, ModelSerializer):
    organisation_consultants = ListField(field=OrganisationConsultantSerializer())

    class Meta(object):
        model_class = Consultant

    def create_organisation_consultant(self, deserialized_data):
        organisation_consultant = OrganisationConsultant()
        self.organisation_consultants.field.update(organisation_consultant, deserialized_data)
        return organisation_consultant

    def update(self, obj, deserialized_data):
        for attr, value in deserialized_data.items():
            if attr == 'organisation_consultants':
                obj.organisation_consultants = []

                # Unique constraint fails unless we flush the deletes before the inserts
                db.session.flush()

                for x in value:
                    organisation_consultant = self.create_organisation_consultant(x)
                    obj.organisation_consultants.append(organisation_consultant)
            elif hasattr(obj, attr):
                setattr(obj, attr, value)

        return obj
