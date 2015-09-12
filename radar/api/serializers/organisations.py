from radar.api.serializers.meta import MetaSerializerMixin
from radar.lib.serializers import ModelSerializer, ListField, BooleanField, ReferenceField
from radar.lib.models import DataSource, Organisation, OrganisationUser, OrganisationPatient


class OrganisationReferenceField(ReferenceField):
    model_class = Organisation


class BasicOrganisationSerializer(ModelSerializer):
    class Meta:
        model_class = Organisation
        exclude = ['organisation_id']


class DataSourceSerializer(ModelSerializer):
    organisation = BasicOrganisationSerializer()

    class Meta:
        model_class = DataSource


class OrganisationSerializer(ModelSerializer):
    data_sources = ListField(field=DataSourceSerializer())

    class Meta:
        model_class = Organisation


class OrganisationUserSerializer(MetaSerializerMixin, ModelSerializer):
    has_view_demographics_permission = BooleanField()
    has_view_patient_permission = BooleanField()
    has_edit_patient_permission = BooleanField()
    has_view_user_permission = BooleanField()
    has_edit_user_membership_permission = BooleanField()
    has_recruit_patient_permission = BooleanField()
    organisation = OrganisationSerializer()

    class Meta:
        model_class = OrganisationUser
        exclude = ['user_id', 'organisation_id']


class OrganisationPatientSerializer(MetaSerializerMixin, ModelSerializer):
    organisation = OrganisationSerializer()

    class Meta:
        model_class = OrganisationPatient
        exclude = ['patient_id', 'organisation_id']
