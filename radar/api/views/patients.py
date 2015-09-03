from flask import request
from flask_login import current_user

from radar.lib.patient_search import PatientQueryBuilder
from radar.lib.permissions import IsAuthenticated, PatientPermission, intersect_units, intersect_disease_groups
from radar.lib.serializers import MetaSerializerMixin, ModelSerializer, StringField, ListField, DateField, IntegerField, \
    Serializer, LookupField, Empty
from radar.lib.views import ListCreateApiView, RetrieveUpdateDestroyAPIView
from radar.models import Patient, UnitPatient, Unit, DiseaseGroup, DiseaseGroupPatient, Facility


class FacilitySerializer(ModelSerializer):
    class Meta:
        model_class = Facility


class UnitSerializer(ModelSerializer):
    facilities = ListField(field=FacilitySerializer())

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
    year_of_birth = IntegerField()
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


class PatientProxy(object):
    def __init__(self, patient, user):
        self.patient = patient
        self.user = user

        unit_users = intersect_units(patient, user, user_membership=True)
        self.demographics = any(x.has_view_demographics_permission for x in unit_users)

    @property
    def first_name(self):
        if self.demographics:
            return self.patient.first_name
        else:
            return Empty

    @property
    def last_name(self):
        if self.demographics:
            return self.patient.last_name
        else:
            return Empty

    @property
    def date_of_birth(self):
        if self.demographics:
            return self.patient.date_of_birth
        else:
            return Empty

    @property
    def disease_groups(self):
        return [x.disease_group for x in self.disease_groups_patients]

    @property
    def disease_group_patients(self):
        if self.user.is_admin:
            return self.patient.disease_group_patients

        units = intersect_units(self.patient, self.user)

        if units:
            return self.patient.disease_group_patients
        else:
            return intersect_disease_groups(self.patient, self.user, patient_membership=True)

    @property
    def year_of_birth(self):
        if self.patient.date_of_birth is not None:
            return self.patient.date_of_birth.year
        else:
            return None

    def __getattr__(self, item):
        return getattr(self.patient, item)


class PatientList(ListCreateApiView):
    serializer_class = PatientSerializer
    model_class = Patient
    permission_classes = [IsAuthenticated, PatientPermission]

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
            builder.disease_group(args['disease_group'])

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

    def get_object_list(self):
        patients, pagination = super(PatientList, self).get_object_list()

        # Wrap patients in proxy object
        patients = [PatientProxy(x, current_user) for x in patients]

        return patients, pagination


class PatientDetail(RetrieveUpdateDestroyAPIView):
    serializer_class = PatientSerializer
    model_class = Patient
    permission_classes = [IsAuthenticated, PatientPermission]

    def get_query(self):
        builder = PatientQueryBuilder(current_user)
        return builder.build()

    def get_object(self):
        patient = super(PatientDetail, self).get_object()
        return PatientProxy(patient, current_user)
