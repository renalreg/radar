from datetime import date, timedelta

import tablib
from cornflake import fields, serializers

from radar.exporter import queries
from radar.models.patients import Patient
from radar.permissions import has_permission_for_patient
from radar.roles import PERMISSION


exporter_map = {}


def register(name):
    def decorator(cls):
        exporter_map[name] = cls
        return cls

    return decorator


def path_getter(path):
    keys = path.split('.')

    def f(value):
        for key in keys:
            if value is None:
                break

            value = getattr(value, key)

        return value

    return f


def none_getter(value):
    return None


def identity_getter(value):
    return value


def query_to_dataset(query, columns):
    data = tablib.Dataset(headers=[c[0] for c in columns])

    for row in query:
        data.append([c[1](row) for c in columns])

    return data


def format_user(user):
    if user.first_name and user.last_name:
        return '%s %s' % (user.first_name, user.last_name)
    else:
        return user.username


def column(name, getter=None):
    if getter is None:
        getter = path_getter(name)
    elif isinstance(getter, basestring):
        getter = path_getter(getter)

    return name, getter


def demographics_column_factory(config):
    if config['anonymised']:
        def column(name, getter=None, anonymised_getter=None, patient_getter=None):
            if anonymised_getter is None:
                anonymised_getter = none_getter
            elif isinstance(anonymised_getter, basestring):
                anonymised_getter = path_getter(anonymised_getter)

            return name, anonymised_getter
    elif config['user'] is not None:
        def column(name, getter=None, anonymised_getter=None, patient_getter=None):
            if getter is None:
                getter = path_getter(name)
            elif isinstance(getter, basestring):
                getter = path_getter(getter)

            if anonymised_getter is None:
                anonymised_getter = none_getter
            elif isinstance(anonymised_getter, basestring):
                anonymised_getter = path_getter(anonymised_getter)

            if patient_getter is None:
                patient_getter = path_getter('patient')
            elif isinstance(anonymised_getter, basestring):
                patient_getter = path_getter(patient_getter)

            def f(value):
                patient = patient_getter(value)

                if has_permission_for_patient(
                    config['user'],
                    patient,
                    PERMISSION.VIEW_DEMOGRAPHICS
                ):
                    return getter(value)
                else:
                    return anonymised_getter(value)

            return name, f
    else:
        def column(name, getter=None, anonymised_getter=None, patient_getter=None):
            if getter is None:
                getter = path_getter(name)
            elif isinstance(getter, basestring):
                getter = path_getter(getter)

            return name, getter

    return column


def get_meta_columns():
    return [
        column('created_date'),
        column('created_user_id'),
        column('created_user', lambda x: format_user(x.created_user)),
        column('modified_date'),
        column('modified_user_id'),
        column('modified_user', lambda x: format_user(x.created_user)),
    ]


class Exporter(object):
    def __init__(self, config):
        self.config = config

    @classmethod
    def parse_config(self, data):
        return {}

    def run(self):
        raise NotImplementedError


@register('patients')
class PatientExporter(Exporter):
    def run(self):
        demographics_column = demographics_column_factory(self.config)

        def d(name, getter=None, anonymised_getter=None):
            return demographics_column(name, getter, anonymised_getter, identity_getter)

        columns = [
            column('id'),
            d('patient_number', 'primary_patient_number.number'),
            d('first_name'),
            d('last_name'),
            d('date_of_birth'),
            column('year_of_birth'),
            d('date_of_death'),
            column('year_of_death'),
            column('gender'),
            column('ethnicity'),
            column('recruited_date'),
            column('recruited_group_id', 'recruited_group.id'),
            column('recruited_group', 'recruited_group.name'),
            column('recruited_user_id', 'recruited_user.id'),
            column('recruited_user', lambda x: format_user(x.recruited_user)),
        ]

        q = queries.get_patients(self.config)

        return query_to_dataset(q, columns)


@register('patient_numbers')
class PatientNumberExporter(Exporter):
    def run(self):
        d = demographics_column_factory(self.config)

        columns = [
            column('id'),
            column('patient_id'),
            column('source_group_id'),
            column('source_group', 'source_group.name'),
            column('source_type'),
            column('number_group_id'),
            column('number_group', 'number_group.name'),
            d('number'),
        ]
        columns.extend(get_meta_columns())

        q = queries.get_patient_numbers(self.config)

        return query_to_dataset(q, columns)


@register('patient_addresses')
class PatientAddressExporter(Exporter):
    def run(self):
        d = demographics_column_factory(self.config)

        columns = [
            column('id'),
            column('patient_id'),
            column('source_group_id'),
            column('source_group', 'source_group.name'),
            column('source_type'),
            column('from_date'),
            column('to_date'),
            d('address_1'),
            d('address_2'),
            d('address_3'),
            d('address_4'),
            d('postcode', anonymised_getter='anonymised_postcode'),
        ]
        columns.extend(get_meta_columns())

        q = queries.get_patient_addresses(self.config)

        return query_to_dataset(q, columns)


@register('patient_aliases')
class PatientAliasExporter(Exporter):
    def run(self):
        d = demographics_column_factory(self.config)

        columns = [
            column('id'),
            column('patient_id'),
            column('source_group_id'),
            column('source_group', 'source_group.name'),
            column('source_type'),
            d('first_name'),
            d('last_name'),
        ]
        columns.extend(get_meta_columns())

        q = queries.get_patient_aliases(self.config)

        return query_to_dataset(q, columns)


@register('patient_demographics')
class PatientDemographicsExporter(Exporter):
    def run(self):
        d = demographics_column_factory(self.config)

        columns = [
            column('id'),
            column('patient_id'),
            column('source_group_id'),
            column('source_group', 'source_group.name'),
            column('source_type'),
            d('first_name'),
            d('last_name'),
            d('date_of_birth'),
            column('year_of_birth'),
            d('date_of_death'),
            column('year_of_death'),
            column('gender'),
            column('ethnicity'),
            d('home_number'),
            d('work_number'),
            d('mobile_number'),
            d('email_address'),
        ]

        columns.extend(get_meta_columns())

        q = queries.get_patient_demographics(self.config)

        return query_to_dataset(q, columns)


@register('medications')
class MedicationExporter(Exporter):
    def run(self):
        columns = [
            column('id'),
            column('patient_id'),
            column('source_group_id'),
            column('source_group', 'source_group.name'),
            column('source_type'),
            column('from_date'),
            column('to_date'),
            column('drug_id'),
            column('drug', 'drug.name'),
            column('drug_text'),
            column('dose_quantity'),
            column('dose_unit'),
            column('dose_text'),
            column('frequency'),
            column('route'),
        ]
        columns.extend(get_meta_columns())

        q = queries.get_medications(self.config)

        return query_to_dataset(q, columns)


@register('patient_diagnoses')
class PatientDiagnosisExporter(Exporter):
    def run(self):
        columns = [
            column('id'),
            column('patient_id'),
            column('source_group_id'),
            column('source_group', 'source_group.name'),
            column('source_type'),
            column('diagnosis_id'),
            column('diagnosis', 'diagnosis.name'),
            column('diagnosis_text'),
            column('symptoms_date'),
            column('from_date'),
            column('to_date'),
            column('gene_test'),
            column('biochemistry'),
            column('clinical_picture'),
            column('biopsy'),
            column('biopsy_diagnosis'),
            column('comments'),
        ]
        columns.extend(get_meta_columns())

        q = queries.get_patient_diagnoses(self.config)

        return query_to_dataset(q, columns)


@register('genetics')
class GeneticsExporter(Exporter):
    def run(self):
        columns = [
            column('id'),
            column('patient_id'),
            column('group_id'),
            column('group', 'group.name'),
            column('date_sent'),
            column('laboratory'),
            column('reference_number'),
            column('karyotype'),
            column('results'),
            column('summary'),
        ]
        columns.extend(get_meta_columns())

        q = queries.get_genetics(self.config)

        return query_to_dataset(q, columns)


@register('pathology')
class PathologyExporter(Exporter):
    def run(self):
        columns = [
            column('id'),
            column('patient_id'),
            column('source_group_id'),
            column('source_group', 'source_group.name'),
            column('date'),
            column('kidney_type'),
            column('kidney_side'),
            column('reference_number'),
            column('image_url'),
            column('histological_summary'),
            column('em_findings'),
        ]
        columns.extend(get_meta_columns())

        q = queries.get_pathology(self.config)

        return query_to_dataset(q, columns)


@register('family_histories')
class FamilyHistoryExporter(Exporter):
    def run(self):
        columns = [
            column('id'),
            column('patient_id'),
            column('group_id'),
            column('group', 'group.name'),
            column('parental_consanguinity'),
            column('family_history'),
        ]
        columns.extend(get_meta_columns())

        q = queries.get_family_histories(self.config)

        return query_to_dataset(q, columns)


@register('family_history_relatives')
class FamilyHistoryRelativeExporter(Exporter):
    def run(self):
        columns = [
            column('id'),
            column('family_history_id'),
            column('relationship'),
            column('patient_id'),
        ]

        q = queries.get_family_history_relatives(self.config)

        return query_to_dataset(q, columns)


@register('ins_clinical_pictures')
class InsClinicalPictureExporter(Exporter):
    def run(self):
        columns = [
            column('id'),
            column('patient_id'),
            column('date_of_picture'),
            column('oedema'),
            column('hypovalaemia'),
            column('fever'),
            column('thrombosis'),
            column('peritonitis'),
            column('pulmonary_odemea'),
            column('hypertension'),
            column('rash'),
            column('rash_details'),
            column('infection'),
            column('infection_details'),
            column('ophthalmoscopy'),
            column('ophthalmoscopy_details'),
            column('comments'),
        ]
        columns.extend(get_meta_columns())

        q = queries.get_ins_clinical_pictures(self.config)

        return query_to_dataset(q, columns)


@register('dialysis')
class DialysisExporter(Exporter):
    def run(self):
        columns = [
            column('id'),
            column('patient_id'),
            column('source_group_id'),
            column('source_group', 'source_group.name'),
            column('source_type'),
            column('from_date'),
            column('to_date'),
            column('modality'),
        ]
        columns.extend(get_meta_columns())

        q = queries.get_dialyses(self.config)

        return query_to_dataset(q, columns)


@register('plasmapheresis')
class PlasmapheresisExporter(Exporter):
    def run(self):
        columns = [
            column('id'),
            column('patient_id'),
            column('source_group_id'),
            column('source_group', 'source_group.name'),
            column('source_type'),
            column('from_date'),
            column('to_date'),
            column('no_of_exchanges'),
            column('response'),
        ]
        columns.extend(get_meta_columns())

        q = queries.get_plasmapheresis(self.config)

        return query_to_dataset(q, columns)


@register('transplants')
class TransplantExporter(Exporter):
    def run(self):
        columns = [
            column('id'),
            column('patient_id'),
            column('source_group_id'),
            column('source_group', 'source_group.name'),
            column('source_type'),
            column('transplant_group_id'),
            column('transplant_group', 'transplant_group.name'),
            column('date'),
            column('type_code', 'modality'),
            column('type_description', 'modality_description'),
            column('date_of_recurrence'),
            column('date_of_failure'),
        ]
        columns.extend(get_meta_columns())

        q = queries.get_transplants(self.config)

        return query_to_dataset(q, columns)


@register('transplant_biopsies')
class TransplantBiopsyExporter(Exporter):
    def run(self):
        columns = [
            column('id'),
            column('transplant_id'),
            column('date_of_biopsy'),
            column('recurrence'),
        ]

        q = queries.get_transplant_biopsies(self.config)

        return query_to_dataset(q, columns)


@register('transplant_rejections')
class TransplantRejectionExporter(Exporter):
    def run(self):
        columns = [
            column('id'),
            column('transplant_id'),
            column('date_of_rejection'),
        ]

        q = queries.get_transplant_rejections(self.config)

        return query_to_dataset(q, columns)


@register('hospitalisations')
class HospitalisationExporter(Exporter):
    def run(self):
        columns = [
            column('id'),
            column('patient_id'),
            column('source_group_id'),
            column('source_group', 'source_group.name'),
            column('source_type'),
            column('date_of_admission'),
            column('date_of_discharge'),
            column('reason_for_admission'),
            column('comments'),
        ]
        columns.extend(get_meta_columns())

        q = queries.get_hospitalisations(self.config)

        return query_to_dataset(q, columns)


@register('ins_relapses')
class InsRelapseExporter(Exporter):
    def run(self):
        columns = [
            column('id'),
            column('patient_id'),
            column('date_of_relapse'),
            column('kidney_type'),
            column('viral_trigger'),
            column('immunisation_trigger'),
            column('other_trigger'),
            column('high_dose_oral_prednisolone'),
            column('iv_methyl_prednisolone'),
            column('date_of_remission'),
            column('remission_type'),
        ]
        columns.extend(get_meta_columns())

        q = queries.get_ins_relapses(self.config)

        return query_to_dataset(q, columns)


@register('mpgn_clinical_pictures')
class MpgnClinicalPicturesExporter(Exporter):
    def run(self):
        columns = [
            column('id'),
            column('patient_id'),
            column('date_of_picture'),
            column('oedema'),
            column('hypertension'),
            column('urticaria'),
            column('partial_lipodystrophy'),
            column('infection'),
            column('infection_details'),
            column('ophthalmoscopy'),
            column('ophthalmoscopy_details'),
            column('comments'),
        ]
        columns.extend(get_meta_columns())

        q = queries.get_mpgn_clinical_pictures(self.config)

        return query_to_dataset(q, columns)


@register('group_patients')
class GroupPatientExporter(Exporter):
    def run(self):
        columns = [
            column('id'),
            column('patient_id'),
            column('group_id'),
            column('group', 'group.name'),
            column('from_date'),
            column('to_date'),
            column('created_group_id'),
            column('created_group', 'created_group.name'),
        ]
        columns.extend(get_meta_columns())

        q = queries.get_group_patients(self.config)

        return query_to_dataset(q, columns)


@register('renal_progressions')
class RenalProgressionExporter(Exporter):
    def run(self):
        columns = [
            column('id'),
            column('patient_id'),
            column('onset_date'),
            column('esrf_date'),
        ]
        columns.extend(get_meta_columns())

        q = queries.get_renal_progressions(self.config)

        return query_to_dataset(q, columns)


@register('results')
class ResultExporter(Exporter):
    def run(self):
        columns = [
            column('id'),
            column('patient_id'),
            column('source_group_id'),
            column('source_group', 'source_group.name'),
            column('source_type'),
            column('date'),
            column('observation_name', 'observation.name'),
            column('value_code', 'value'),
            column('value_description')
        ]
        columns.extend(get_meta_columns())

        q = queries.get_results(self.config)

        return query_to_dataset(q, columns)


def previous_month():
    now = date.today()
    previous_end = now.replace(day=1) - timedelta(days=1)
    previous_start = previous_end.replace(day=1)
    return previous_start


class NIHRConfigSerializer(serializers.Serializer):
    from_date = fields.DateField(default=previous_month)


@register('nihr')
class NIHRExporter(Exporter):
    @classmethod
    def parse_config(cls, data):
        serializer = NIHRConfigSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        return serializer.validated_data

    def run(self):
        columns = [
            column('id'),
            column('recruited_date'),
            column('recruited_group_id', 'recruited_group.id'),
            column('recruited_group', 'recruited_group.name'),
        ]

        from_date = self.config['from_date']

        q = Patient.query
        q = q.filter(Patient.recruited_date >= from_date)
        q = q.order_by(Patient.recruited_date)

        return query_to_dataset(q, columns)
