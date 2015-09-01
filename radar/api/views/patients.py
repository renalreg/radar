from flask import request
from flask_login import current_user
from radar.lib.ordering import DESCENDING, ASCENDING
from radar.lib.patient_search import PatientQueryBuilder
from radar.lib.serializers import MetaSerializerMixin, ModelSerializer, StringField, ListField, DateField, IntegerField, \
    Serializer, LookupField
from radar.lib.views import ListCreateApiView, RetrieveUpdateDestroyAPIView
from radar.models import Patient, UnitPatient, Unit, DiseaseGroup, DiseaseGroupPatient


class UnitSerializer(MetaSerializerMixin, ModelSerializer):
    class Meta:
        model_class = Unit


class UnitPatientSerializer(MetaSerializerMixin, ModelSerializer):
    unit = UnitSerializer()

    class Meta:
        model_class = UnitPatient
        exclude = ['patient_id', 'unit_id']


class DiseaseGroupSerializer(MetaSerializerMixin, ModelSerializer):
    class Meta:
        model_class = DiseaseGroup


class DiseaseGroupPatientSerializer(MetaSerializerMixin, ModelSerializer):
    disease_group = DiseaseGroupSerializer()

    class Meta:
        model_class = DiseaseGroupPatient
        exclude = ['patient_id', 'disease_group_id']


class PatientSerializer(MetaSerializerMixin, ModelSerializer):
    first_name = StringField()
    last_name = StringField()
    date_of_birth = DateField()
    gender = StringField()
    units = ListField(field=UnitPatientSerializer(), source='unit_patients')
    disease_groups = ListField(field=DiseaseGroupPatientSerializer(), source='disease_group_patients')

    class Meta:
        model_class = Patient
        fields = ['id']


class DiseaseGroupLookupField(LookupField):
    model_class = DiseaseGroup


class UnitLookupField(LookupField):
    model_class = Unit


class PatientListRequestSerializer(Serializer):
    id = IntegerField()
    first_name = StringField()
    last_name = StringField()
    date_of_birth = DateField()
    year_of_birth = IntegerField()
    date_of_death = DateField()
    gender = StringField()
    patient_number = StringField()
    unit_id = UnitLookupField(write_only=True)
    disease_group_id = DiseaseGroupLookupField(write_only=True)


class PatientList(ListCreateApiView):
    serializer_class = PatientSerializer

    def get_query(self):
        serializer = PatientListRequestSerializer()
        args = serializer.to_value(request.args)

        builder = PatientQueryBuilder(current_user)

        if 'first_name' in args:
            builder.first_name(args['first_name'])

        if 'last_name' in args:
            builder.last_name(args['last_name'])

        if 'unit' in args:
            builder.unit(args['unit'])

        if 'disease_group' in args:
            builder.unit(args['disease_group'])

        if 'date_of_birth' in args:
            builder.date_of_birth(args['date_of_birth'])

        if 'patient_number' in args:
            builder.patient_number(args['patient_number'])

        if 'gender' in args:
            builder.gender(args['gender'])

        if 'id' in args:
            builder.radar_id(args['id'])

        if 'year_of_birth' in args:
            builder.year_of_death(args['year_of_birth'])

        if 'date_of_death' in args:
            builder.date_of_death(args['date_of_death'])

        if 'year_of_death' in args:
            builder.year_of_death(args['year_of_death'])

        if 'is_active' in args:
            builder.is_active(args['is_active'])

        sort, reverse = self.get_sort_args()

        if sort is not None:
            builder.sort(sort, reverse)

        query = builder.build()

        return query


class PatientDetail(RetrieveUpdateDestroyAPIView):
    serializer_class = PatientSerializer

    def get_query(self):
        return Patient.query
