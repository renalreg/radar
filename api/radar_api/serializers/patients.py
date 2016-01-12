from radar_api.serializers.meta import MetaSerializerMixin
from radar_api.serializers.group_patients import GroupPatientSerializer
from radar_api.serializers.groups import GroupReferenceField, TinyGroupReferenceField
from radar.patients import PatientProxy
from radar.serializers.core import Serializer
from radar.serializers.fields import StringField, BooleanField, IntegerField, \
    DateField, ListField, DateTimeField, CommaSeparatedField
from radar.serializers.models import ModelSerializer
from radar.serializers.fields import LabelledStringField, LabelledIntegerField
from radar.models.patients import Patient, GENDERS, ETHNICITIES


class TinyGroupPatientSerializer(Serializer):
    id = IntegerField()
    group = TinyGroupReferenceField()


class TinyPatientSerializer(Serializer):
    id = IntegerField(read_only=True)
    first_name = StringField(read_only=True)
    last_name = StringField(read_only=True)
    date_of_birth = DateField(read_only=True)
    year_of_birth = IntegerField(read_only=True)
    date_of_death = DateField(read_only=True)
    year_of_death = IntegerField(read_only=True)
    gender = LabelledIntegerField(GENDERS, read_only=True)
    ethnicity = LabelledStringField(ETHNICITIES, read_only=True)
    groups = ListField(field=TinyGroupPatientSerializer(), source='group_patients', read_only=True)
    recruited_date = DateTimeField(read_only=True)
    recruited_group = TinyGroupReferenceField(read_only=True)
    comments = StringField()

    def __init__(self, current_user, **kwargs):
        super(TinyPatientSerializer, self).__init__(**kwargs)
        self.current_user = current_user

    def to_data(self, value):
        value = PatientProxy(value, self.current_user)
        return super(TinyPatientSerializer, self).to_data(value)


class PatientSerializer(MetaSerializerMixin, ModelSerializer):
    first_name = StringField(read_only=True)
    last_name = StringField(read_only=True)
    date_of_birth = DateField(read_only=True)
    year_of_birth = IntegerField(read_only=True)
    date_of_death = DateField(read_only=True)
    year_of_death = IntegerField(read_only=True)
    gender = LabelledIntegerField(GENDERS, read_only=True)
    ethnicity = LabelledStringField(ETHNICITIES, read_only=True)
    groups = ListField(field=GroupPatientSerializer(), source='group_patients', read_only=True)
    recruited_date = DateTimeField(read_only=True)
    recruited_group = GroupReferenceField(read_only=True)
    comments = StringField()

    class Meta(object):
        model_class = Patient
        fields = ['id', 'created_date', 'modified_date']

    def __init__(self, current_user, **kwargs):
        super(PatientSerializer, self).__init__(**kwargs)
        self.current_user = current_user

    def to_data(self, value):
        value = PatientProxy(value, self.current_user)
        return super(PatientSerializer, self).to_data(value)


class PatientListRequestSerializer(Serializer):
    id = IntegerField()
    first_name = StringField()
    last_name = StringField()
    date_of_birth = DateField()
    year_of_birth = IntegerField()
    date_of_death = DateField()
    year_of_death = IntegerField()
    gender = StringField()
    patient_number = StringField()
    group = GroupReferenceField()
    groups = CommaSeparatedField(GroupReferenceField())
    is_active = BooleanField()
