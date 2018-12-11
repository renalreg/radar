from __future__ import division

from collections import OrderedDict
from datetime import date, datetime
import re

import tablib

from radar.exporter import queries
from radar.exporter.utils import get_months, get_years, identity_getter, none_getter, path_getter
from radar.models.results import Observation
from radar.models.rituximab import SUPPORTIVE_MEDICATIONS
from radar.permissions import has_permission_for_patient
from radar.roles import PERMISSION
from radar.utils import get_attrs

try:
    basestring
except NameError:
    basestring = str
    unicode = str


ILLEGAL_CHARACTERS_RE = re.compile(r'[\000-\010]|[\013-\014]|[\016-\037]')

exporter_map = {}


def stringify_list(name):

    def stringify(entry):
        items = entry.data.get(name) or []
        return '; '.join(sorted(items))

    return stringify


def none_to_empty(value):
    return '' if value is None else value


def formatters(value):
    val = format_date(value)
    val = none_to_empty(val)
    return val


def make_dataset(columns, results=False):
    data = tablib.Dataset(headers=[c[0] for c in columns])
    if not results:
        for i, header in enumerate(data.headers):
            if 'date' in header:
                data.add_formatter(i, formatters)
            else:
                data.add_formatter(i, none_to_empty)
    else:
        for i, header in enumerate(data.headers):
            data.add_formatter(i, none_to_empty)
    return data


def register(name):
    """Add an exporter."""

    def decorator(cls):
        exporter_map[name] = cls
        return cls

    return decorator


def query_to_dataset(query, columns):
    data = make_dataset(columns)

    for row in query:
        data.append([c[1](row) for c in columns])
    return data


def format_user(user):
    if user is None:
        return None
    elif user.first_name and user.last_name:
        return '%s %s' % (user.first_name, user.last_name)
    else:
        return user.username


def format_date(dt):
    val = dt
    fmt = '%d/%m/%Y'
    if isinstance(dt, (date, datetime)):
        try:
            val = dt.strftime(fmt)
        except ValueError:
            val = '{:02d}/{:02d}/{}'.format(dt.day, dt.month, dt.year)
    elif re.match(r'^\d{4}\-(0?[1-9]|1[012])\-(0?[1-9]|[12][0-9]|3[01])$', unicode(dt)):
        try:
            parsed = datetime.strptime(dt, '%Y-%m-%d')
        except ValueError:
            year, month, day = dt.split('-')
            parsed = date(int(year), int(month), int(day))
        try:
            val = parsed.strftime(fmt)
        except ValueError:
            val = '{:02d}/{:02d}/{}'.format(parsed.day, parsed.month, parsed.year)

    return val


def column(name, getter=None):
    if getter is None:
        getter = path_getter(name)
    elif isinstance(getter, basestring):
        getter = path_getter(getter)

    return name, getter


def demographics_column_factory(config):
    """Returns a column based on the config."""

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


def get_meta_columns(config):
    def created_user(x):
        if config['anonymised']:
            return ""
        return format_user(x.created_user)

    def modified_user(x):
        if config['anonymised']:
            return ""
        return format_user(x.modified_user)

    return [
        column('created_date', lambda x: format_date(x.created_date)),
        column('created_user_id'),
        column('created_user', created_user),
        column('modified_date', lambda x: format_date(x.modified_date)),
        column('modified_user_id'),
        column('modified_user', modified_user),
    ]


def query_to_plain_rows(query, columns):
    if query is None:
        return None
    else:
        output_list = list()
        for row in query:
            insert_row = list()
            for x in [c[1](row) for c in columns]:
                if getattr(x, 'code', None):
                    insert_row.append(x.code)
                else:
                    insert_row.append(x)

            output_list.append(insert_row)

        return output_list


class Exporter(object):
    def __init__(self, config):
        self.config = config
        self._query = None
        self._columns = None

    @classmethod
    def parse_config(self, data):
        return {}

    def run(self):
        raise NotImplementedError

    @property
    def dataset(self):
        return query_to_dataset(self._query, self._columns)

    @property
    def plain_rows(self):
        return query_to_plain_rows(self._query, self._columns)

    def get_create_table_string(self, name):
        columns = self._columns

        # Make Column Names SQL Compatible
        column_row = list()
        for column_name in [row[0] for row in columns]:
            for character in ("-", " ", ":", ">", "/", "<", "(", ")"):
                column_name = column_name.replace(character, "_")
            column_row.append(column_name)

        # Build Query
        sqlstring = """
        CREATE TABLE """ + name + """
        (
        """ + " TEXT,\n".join(column_row) + """ TEXT
        )
        """

        return sqlstring

    def get_insert_string(self, name):
        sqlstring = """
        INSERT INTO """ + name + """
        VALUES (""" + "?,".join(len(self._columns) * ['']) + """?  )
        """

        return sqlstring


@register('patients')
class PatientExporter(Exporter):
    def run(self):
        demographics_column = demographics_column_factory(self.config)

        def d(name, getter=None, anonymised_getter=None):
            return demographics_column(name, getter, anonymised_getter, identity_getter)
        group = self.config['patient_group']

        def recruited_user(x):
            if self.config['anonymised']:
                return ""
            return format_user(x.recruited_user(group))

        self._columns = [
            column('patient_id', 'id'),
            d('patient_number', 'primary_patient_number.number'),
            d('first_name'),
            d('last_name'),
            d('date_of_birth', lambda x: format_date(x.date_of_birth)),
            column('year_of_birth'),
            d('date_of_death', lambda x: format_date(x.date_of_death)),
            column('year_of_death'),
            column('gender'),
            column('gender_label'),
            column('available_ethnicity'),
            column('patient_view', 'ukrdc'),
            column('control'),
            column('recruited_date', lambda x: format_date(x.recruited_date(group))),  # 13
            column('recruited_group_id', lambda x: get_attrs(x.recruited_group(group), 'id')),
            column('recruited_group', lambda x: get_attrs(x.recruited_group(group), 'name')),
            column('recruited_user_id', lambda x: get_attrs(x.recruited_user(group), 'id')),
            column('recruited_user', recruited_user),
        ]

        q = queries.get_patients(self.config)
        self._query = q


@register('patient_numbers')
class PatientNumberExporter(Exporter):
    def run(self):
        d = demographics_column_factory(self.config)

        self._columns = [
            column('id'),
            column('patient_id'),
            column('source_group_id'),
            column('source_group', 'source_group.name'),
            column('source_type'),
            column('number_group_id'),
            column('number_group', 'number_group.name'),
            d('number'),
        ]
        self._columns.extend(get_meta_columns(self.config))

        q = queries.get_patient_numbers(self.config)
        self._query = q


@register('patient_addresses')
class PatientAddressExporter(Exporter):
    def run(self):
        d = demographics_column_factory(self.config)

        self._columns = [
            column('id'),
            column('patient_id'),
            column('source_group_id'),
            column('source_group', 'source_group.name'),
            column('source_type'),
            column('from_date', lambda x: format_date(x.from_date)),
            column('to_date', lambda x: format_date(x.to_date)),
            d('address1'),
            d('address2'),
            d('address3'),
            d('address4'),
            d('postcode', anonymised_getter='anonymised_postcode'),
        ]
        self._columns.extend(get_meta_columns(self.config))

        q = queries.get_patient_addresses(self.config)
        self._query = q


@register('patient_aliases')
class PatientAliasExporter(Exporter):
    def run(self):
        d = demographics_column_factory(self.config)

        self._columns = [
            column('id'),
            column('patient_id'),
            column('source_group_id'),
            column('source_group', 'source_group.name'),
            column('source_type'),
            d('first_name'),
            d('last_name'),
        ]
        self._columns.extend(get_meta_columns(self.config))

        q = queries.get_patient_aliases(self.config)
        self._query = q


@register('patient_demographics')
class PatientDemographicsExporter(Exporter):
    def run(self):
        d = demographics_column_factory(self.config)

        self._columns = [
            column('id'),
            column('patient_id'),
            column('source_group_id'),
            column('source_group', 'source_group.name'),
            column('source_type'),
            d('first_name'),
            d('last_name'),
            d('date_of_birth', lambda x: format_date(x.date_of_birth)),
            column('year_of_birth'),
            d('date_of_death', lambda x: format_date(x.date_of_death)),
            column('year_of_death'),
            column('gender'),
            column('gender_label'),
            column('ethnicity'),
            column('ethnicity_label'),
            d('home_number'),
            d('work_number'),
            d('mobile_number'),
            d('email_address'),
        ]

        self._columns.extend(get_meta_columns(self.config))

        q = queries.get_patient_demographics(self.config)
        self._query = q


@register('medications')
class MedicationExporter(Exporter):
    def run(self):
        self._columns = [
            column('id'),
            column('patient_id'),
            column('source_group_id'),
            column('source_group', 'source_group.name'),
            column('source_type'),
            column('from_date', lambda x: format_date(x.from_date)),
            column('to_date', lambda x: format_date(x.to_date)),
            column('drug_id'),
            column('drug', 'drug.name'),
            column('drug_text'),
            column('dose_quantity'),
            column('dose_unit'),
            column('dose_unit_label'),
            column('dose_text'),
            column('frequency'),
            column('route'),
            column('route_label'),
        ]
        self._columns.extend(get_meta_columns(self.config))

        q = queries.get_medications(self.config)
        self._query = q


@register('current-medications')
class CurrentMedicationExporter(Exporter):
    def run(self):
        self._columns = [
            column('id'),
            column('patient_id'),
            column('date_of_visit', lambda x: format_date(x.date_recorded)),
            column('source_group_id'),
            column('source_group', 'source_group.name'),
            column('source_type'),
            column('drug_id'),
            column('drug', 'drug.name'),
            column('drug_text'),
            column('dose_quantity'),
            column('dose_unit'),
            column('dose_unit_label'),
            column('dose_text'),
            column('frequency'),
            column('route'),
            column('route_label'),
        ]
        self._columns.extend(get_meta_columns(self.config))

        q = queries.get_current_medications(self.config)
        self._query = q


class DiagnosisExporter(Exporter):
    def run(self):
        self._columns = [
            column('id'),
            column('patient_id'),
            column('source_group_id'),
            column('source_group', 'source_group.name'),
            column('source_type'),

            column('era-edta prd'),  # 5
            column('icd-10'),        # 6
            column('snomed ct'),     # 7

            column('diagnosis', 'diagnosis.name'),
            column('diagnosis_text'),
            column('symptoms_date', lambda x: format_date(x.symptoms_date)),
            column('symptoms_age_years', lambda x: get_years(x.symptoms_age)),
            column('symptoms_age_months', lambda x: get_months(x.symptoms_age)),
            column('from_date', lambda x: format_date(x.from_date)),
            column('from_age_years', lambda x: get_years(x.from_age)),
            column('from_age_months', lambda x: get_months(x.from_age)),
            column('to_date', lambda x: format_date(x.to_date)),
            column('to_age_years', lambda x: get_years(x.to_age)),
            column('to_age_months', lambda x: get_months(x.to_age)),
            column('gene_test'),
            column('biochemistry'),
            column('clinical_picture'),
            column('biopsy'),
            column('biopsy_diagnosis'),
            column('biopsy_diagnosis_label'),
            column('comments'),
        ]
        self._columns.extend(get_meta_columns(self.config))
        q = queries.get_patient_diagnoses(self.config)
        self._patient_diagnoses_query = q
        primary_diagnoses = queries.get_primary_diagnoses(self.config)
        self._primary_diagnoses_query = primary_diagnoses

        primary = make_dataset(self._columns)
        comorbidity = make_dataset(self._columns)

        for patient_diagnosis in q:
            values = [c[1](patient_diagnosis) for c in self._columns]

            diagnosis = patient_diagnosis.diagnosis

            if diagnosis and diagnosis.codes:
                for code in diagnosis.codes:
                    if code.system == 'ERA-EDTA PRD':
                        values[5] = code.code
                    elif code.system == 'ICD-10':
                        values[6] = code.code
                    elif code.system == 'SNOMED CT':
                        values[7] = code.code

            if diagnosis in primary_diagnoses:
                primary.append(values)
            else:
                comorbidity.append(values)

        self._primary = primary
        self._comorbidity = comorbidity


@register('primary-diagnoses')
class PrimaryDiagnosisExporter(DiagnosisExporter):

    @property
    def dataset(self):
        return self._primary

    @property
    def plain_rows(self):
        if self._patient_diagnoses_query is None:
            return None
        else:
            output_list = list()
            for patient_diagnosis in self._patient_diagnoses_query:
                insert_row = list()
                for x in [c[1](patient_diagnosis) for c in self._columns]:
                    if getattr(x, 'code', None):
                        insert_row.append(x.code)
                    else:
                        insert_row.append(x)

                diagnosis = patient_diagnosis.diagnosis

                if diagnosis and diagnosis.codes:
                    for code in diagnosis.codes:
                        if code.system == 'ERA-EDTA PRD':
                            insert_row[5] = code.code
                        elif code.system == 'ICD-10':
                            insert_row[6] = code.code
                        elif code.system == 'SNOMED CT':
                            insert_row[7] = code.code

                if diagnosis in self._primary_diagnoses_query:
                    output_list.append(insert_row)

            return output_list


@register('comorbidities')
class ComorbiditiesExporter(DiagnosisExporter):

    @property
    def dataset(self):
        return self._comorbidity


@register('genetics')
class GeneticsExporter(Exporter):
    def run(self):
        self._columns = [
            column('id'),
            column('patient_id'),
            column('group_id'),
            column('group', 'group.name'),
            column('date_sent', lambda x: format_date(x.date_sent)),
            column('laboratory'),
            column('reference_number'),
            column('karyotype'),
            column('karyotype_label'),
            column('results'),
            column('summary'),
        ]
        self._columns.extend(get_meta_columns(self.config))

        q = queries.get_genetics(self.config)
        self._query = q


@register('pathology')
class PathologyExporter(Exporter):
    def run(self):
        self._columns = [
            column('id'),
            column('patient_id'),
            column('source_group_id'),
            column('source_group', 'source_group.name'),
            column('date', lambda x: format_date(x.date)),
            column('kidney_type'),
            column('kidney_type_label'),
            column('kidney_side'),
            column('kidney_side_label'),
            column('reference_number'),
            column('image_url'),
            column('histological_summary'),
            column('em_findings'),
        ]
        self._columns.extend(get_meta_columns(self.config))

        q = queries.get_pathology(self.config)
        self._query = q

    @property
    def dataset(self):
        data = make_dataset(self._columns)
        for row in self._query:
            record = [c[1](row) for c in self._columns]
            if record[11]:
                record[11] = re.sub(ILLEGAL_CHARACTERS_RE, '', record[11])
            data.append(record)
        return data


@register('family_histories')
class FamilyHistoryExporter(Exporter):
    def run(self):
        self._columns = [
            column('id'),
            column('patient_id'),
            column('group_id'),
            column('group', 'group.name'),
            column('parental_consanguinity'),
            column('family_history'),
        ]
        self._columns.extend(get_meta_columns(self.config))

        q = queries.get_family_histories(self.config)
        self._query = q


@register('family_history_relatives')
class FamilyHistoryRelativeExporter(Exporter):
    def run(self):
        self._columns = [
            column('id'),
            column('family_history_id'),
            column('relationship'),
            column('relationship_label'),
            column('patient_id'),
        ]

        q = queries.get_family_history_relatives(self.config)
        self._query = q


@register('ins_clinical_pictures')
class InsClinicalPictureExporter(Exporter):
    def run(self):
        self._columns = [
            column('id'),
            column('patient_id'),
            column('date_of_picture', lambda x: format_date(x.date_of_picture)),
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
        self._columns.extend(get_meta_columns(self.config))

        q = queries.get_ins_clinical_pictures(self.config)
        self._query = q


@register('dialysis')
class DialysisExporter(Exporter):
    def run(self):
        self._columns = [
            column('id'),
            column('patient_id'),
            column('source_group_id'),
            column('source_group', 'source_group.name'),
            column('source_type'),
            column('from_date', lambda x: format_date(x.from_date)),
            column('to_date', lambda x: format_date(x.to_date)),
            column('modality'),
            column('modality_label'),
        ]
        self._columns.extend(get_meta_columns(self.config))

        q = queries.get_dialyses(self.config)
        self._query = q


@register('plasmapheresis')
class PlasmapheresisExporter(Exporter):
    def run(self):
        self._columns = [
            column('id'),
            column('patient_id'),
            column('source_group_id'),
            column('source_group', 'source_group.name'),
            column('source_type'),
            column('from_date', lambda x: format_date(x.from_date)),
            column('to_date', lambda x: format_date(x.to_date)),
            column('no_of_exchanges'),
            column('no_of_exchanges_label'),
            column('response'),
            column('response_label'),
        ]
        self._columns.extend(get_meta_columns(self.config))

        q = queries.get_plasmapheresis(self.config)
        self._query = q


@register('transplants')
class TransplantExporter(Exporter):
    def run(self):
        self._columns = [
            column('id'),
            column('patient_id'),
            column('source_group_id'),
            column('source_group', 'source_group.name'),
            column('source_type'),
            column('transplant_group_id'),
            column('transplant_group', 'transplant_group.name'),
            column('date', lambda x: format_date(x.date)),
            column('modality'),
            column('modality_label'),
            column('date_of_recurrence', lambda x: format_date(x.date_of_recurrence)),
            column('date_of_failure', lambda x: format_date(x.date_of_failure)),
        ]
        self._columns.extend(get_meta_columns(self.config))

        q = queries.get_transplants(self.config)
        self._query = q


@register('transplant_biopsies')
class TransplantBiopsyExporter(Exporter):
    def run(self):
        self._columns = [
            column('id'),
            column('transplant_id'),
            column('date_of_biopsy', lambda x: format_date(x.date_of_biopsy)),
            column('recurrence'),
        ]

        q = queries.get_transplant_biopsies(self.config)
        self._query = q


@register('transplant_rejections')
class TransplantRejectionExporter(Exporter):
    def run(self):
        self._columns = [
            column('id'),
            column('transplant_id'),
            column('date_of_rejection', lambda x: format_date(x.date_of_rejection)),
        ]

        q = queries.get_transplant_rejections(self.config)
        self._query = q


@register('hospitalisations')
class HospitalisationExporter(Exporter):
    def run(self):
        self._columns = [
            column('id'),
            column('patient_id'),
            column('source_group_id'),
            column('source_group', 'source_group.name'),
            column('source_type'),
            column('date_of_admission', lambda x: format_date(x.date_of_admission)),
            column('date_of_discharge', lambda x: format_date(x.date_of_discharge)),
            column('reason_for_admission'),
            column('comments'),
        ]
        self._columns.extend(get_meta_columns(self.config))

        q = queries.get_hospitalisations(self.config)
        self._query = q


@register('ins_relapses')
class InsRelapseExporter(Exporter):
    def run(self):
        self._columns = [
            column('id'),
            column('patient_id'),
            column('date_of_relapse'),
            column('kidney_type'),
            column('kidney_type_label'),
            column('viral_trigger'),
            column('immunisation_trigger'),
            column('other_trigger'),
            column('high_dose_oral_prednisolone'),
            column('iv_methyl_prednisolone'),
            column('date_of_remission', lambda x: format_date(x.date_of_remission)),
            column('remission_type'),
            column('remission_type_label'),
        ]
        self._columns.extend(get_meta_columns(self.config))

        q = queries.get_ins_relapses(self.config)
        self._query = q


@register('mpgn_clinical_pictures')
class MpgnClinicalPicturesExporter(Exporter):
    def run(self):
        self._columns = [
            column('id'),
            column('patient_id'),
            column('date_of_picture', lambda x: format_date(x.date_of_picture)),
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
        self._columns.extend(get_meta_columns(self.config))

        q = queries.get_mpgn_clinical_pictures(self.config)
        self._query = q


@register('group_patients')
class GroupPatientExporter(Exporter):
    def run(self):
        self._columns = [
            column('id'),
            column('patient_id'),
            column('group_id'),
            column('group', 'group.name'),
            column('from_date', lambda x: format_date(x.from_date)),
            column('to_date', lambda x: format_date(x.to_date)),
            column('created_group_id'),
            column('created_group', 'created_group.name'),
        ]
        self._columns.extend(get_meta_columns(self.config))

        q = queries.get_group_patients(self.config)
        self._query = q


@register('renal_progressions')
class RenalProgressionExporter(Exporter):
    def run(self):
        self._columns = [
            column('id'),
            column('patient_id'),
            column('onset_date', lambda x: format_date(x.onset_date)),
            column('ckd3a_date', lambda x: format_date(x.ckd3a_date)),
            column('ckd3b_date', lambda x: format_date(x.ckd3b_date)),
            column('ckd4_date', lambda x: format_date(x.ckd4_date)),
            column('ckd5_date', lambda x: format_date(x.ckd5_date)),
            column('esrf_date', lambda x: format_date(x.esrf_date)),
        ]
        self._columns.extend(get_meta_columns(self.config))

        q = queries.get_renal_progressions(self.config)
        self._query = q


@register('results')
class ResultExporter(Exporter):
    def run(self):
        self._columns = [
            column('id'),
            column('patient_id'),
            column('source_group_id'),
            column('source_group', 'source_group.name'),
            column('source_type'),
            column('date'),
            column('observation_name', 'observation.name'),
            column('value'),
            column('value_label'),
            column('sent_value')
        ]
        self._columns.extend(get_meta_columns(self.config))

        q = queries.get_results(self.config)
        self._query = q


@register('results-pivot')
class PivotedResultExporter(Exporter):
    def run(self):
        q = queries.get_results(self.config)

        self._columns = [
            column('patient_id'),
            column('source_group'),
            column('source_type'),
            column('date'),
        ]
        self._query = q

    @property
    def dataset(self):
        egfr_calculated = 'Estimated GFR Calculated'
        extra = {row.observation.name for row in self._query}
        extra.add(egfr_calculated)
        extra = sorted(extra, key=lambda val: val.lower())

        self._columns.extend(column(name) for name in extra)

        data = OrderedDict()

        for row in self._query:
            key = (row.patient_id, row.source_group.name, row.source_type, row.date)
            if key not in data:
                data[key] = {egfr_calculated: ''}

            data[key][row.observation.name] = row.value_label_or_value

            if data[key][egfr_calculated] == '':
                data[key][egfr_calculated] = row.egfr_calculated

        dataset = make_dataset(self._columns, results=True)

        for key, results in data.items():
            row = list(key)
            try:
                row[3] = row[3].strftime('%d/%m/%Y %H:%M:%S')
            except ValueError:
                year, month, day, hour, minute, second = row[3].timetuple()[:6]
                row[3] = '{}/{}/{} {}:{}:{}'.format(day, month, year, hour, minute, second)

            for test in extra:
                if test in results:
                    row.append(results[test])
                else:
                    row.append('')
            dataset.append(row)

        return dataset

    @property
    def plain_rows(self):
        raise NotImplementedError


@register('resultslist')
class ResultListExporter(Exporter):
    def run(self):
        q = queries.get_results(self.config)

        self._columns = [
            column('patient_id'),
            column('source_group'),
            column('source_type'),
            column('date'),
            column('pv_code'),
            column('value')
        ]
        self._query = q

    @property
    def plain_rows(self):

        for result in self._query.yield_per(1000):
            output_row = list()
            output_row.append(result.patient_id)
            output_row.append(result.source_group.code)
            output_row.append(result.source_type)
            output_row.append(result.date)
            output_row.append(result.observation.pv_code)
            output_row.append(result.value)

            yield output_row

            # Add Row for Calculated eGFR, if present
            if result.observation.pv_code == 'CREATININE':
                output_row = list()
                output_row.append(result.patient_id)
                output_row.append(result.source_group.code)
                output_row.append(result.source_type)
                output_row.append(result.date)
                # Keep distinct from unit supplied eGFRs
                output_row.append('EGFR_RDR')
                output_row.append(result.egfr_calculated)

                yield output_row


@register('observations')
class ObservationExporter(Exporter):
    def run(self):
        self._columns = [
            column('id'),
            column('name'),
            column('short_name'),
            column('value_type'),
            column('sample_type'),
            column('pv_code'),
            column('min_value'),
            column('max_value'),
            column('min_length'),
            column('max_length'),
            column('units'),
            column('options'),
        ]

        self._query = Observation.query.order_by(Observation.id)


@register('6cit')
class Cit6Exporter(Exporter):
    def run(self):
        self._columns = [
            column('id'),
            column('patient_id'),
            column('date', 'data.date'),
            column('q1', 'data.q1'),
            column('q2', 'data.q2'),
            column('q4', 'data.q4'),
            column('q5', 'data.q5'),
            column('q6', 'data.q6'),
            column('q7', 'data.q7'),
            column('score', 'data.score'),
        ]
        self._columns.extend(get_meta_columns(self.config))
        q = queries.get_form_data(self.config)
        self._query = q


@register('chu9d')
class CHU9DExporter(Exporter):
    def run(self):
        self._columns = [
            column('id'),
            column('patient_id'),
            column('date', 'data.date'),
            column('worried', 'data.worried'),
            column('sad', 'data.sad'),
            column('pain', 'data.pain'),
            column('tired', 'data.tired'),
            column('annoyed', 'data.annoyed'),
            column('work', 'data.work'),
            column('sleep', 'data.sleep'),
            column('routine', 'data.routine'),
            column('activities', 'data.activities'),

        ]
        self._columns.extend(get_meta_columns(self.config))
        q = queries.get_form_data(self.config)
        self._query = q


@register('diabetic-complications')
class DiabeticComplicationExporter(Exporter):
    def run(self):
        self._columns = [
            column('id'),
            column('patient_id'),
            column('laser', 'data.laser'),
            column('foot ulcers', 'data.footUlcers'),
            column('retinopathy', 'data.retinopathy'),
            column('peripheral neuropathy', 'data.peripheralNeuropathy'),
        ]
        self._columns.extend(get_meta_columns(self.config))
        q = queries.get_form_data(self.config)
        self._query = q


@register('eq-5d-5l')
class Eq5d5lExporter(Exporter):
    def run(self):
        self._columns = [
            column('id'),
            column('patient_id'),
            column('date', 'data.date'),
            column('age', 'data.age'),
            column('gender', 'data.gender'),
            column('mobility', 'data.mobility'),
            column('self care', 'data.selfCare'),
            column('pain discomfort', 'data.painDiscomfort'),
            column('usual activities', 'data.usualActivities'),
            column('anxiety depression', 'data.anxietyDepression'),
            column('health', 'data.health'),
        ]
        self._columns.extend(get_meta_columns(self.config))
        q = queries.get_form_data(self.config)
        self._query = q


@register('eq-5d-y')
class Eq5dyExporter(Exporter):
    def run(self):
        self._columns = [
            column('id'),
            column('patient_id'),
            column('date', 'data.date'),
            column('age', 'data.age'),
            column('gender', 'data.gender'),
            column('mobility', 'data.mobility'),
            column('self care', 'data.selfCare'),
            column('pain discomfort', 'data.painDiscomfort'),
            column('usual activities', 'data.usualActivities'),
            column('anxiety depression', 'data.anxietyDepression'),
            column('health', 'data.health'),
        ]
        self._columns.extend(get_meta_columns(self.config))
        q = queries.get_form_data(self.config)
        self._query = q


@register('hads')
class HadsExporter(Exporter):
    def run(self):
        self._columns = [
            column('id'),
            column('patient_id'),
            column('date', 'data.date'),
            column('a1', 'data.a1'),
            column('a2', 'data.a2'),
            column('a3', 'data.a3'),
            column('a4', 'data.a4'),
            column('a5', 'data.a5'),
            column('a6', 'data.a6'),
            column('a7', 'data.a7'),
            column('d1', 'data.d1'),
            column('d2', 'data.d2'),
            column('d3', 'data.d3'),
            column('d4', 'data.d4'),
            column('d5', 'data.d5'),
            column('d6', 'data.d6'),
            column('d7', 'data.d7'),
            column('anxiety score', 'data.anxietyScore'),
            column('depression score', 'data.depressionScore'),
        ]
        self._columns.extend(get_meta_columns(self.config))
        q = queries.get_form_data(self.config)
        self._query = q


@register('family-history')
class FamilyDiseasesHistoryExporter(Exporter):
    def run(self):
        self._columns = [
            column('id'),
            column('patient_id'),
            column('chd', 'data.chd'),
            column('eskd', 'data.eskd'),
            column('diabetes', 'data.diabetes'),
            column('chdRelative1', 'data.chdRelative1'),
            column('chdRelative2', 'data.chdRelative2'),
            column('chdRelative3', 'data.chdRelative3'),
            column('eskdRelative1', 'data.eskdRelative1'),
            column('eskdRelative2', 'data.eskdRelative2'),
            column('eskdRelative3', 'data.eskdRelative3'),
            column('diabetesRelative1', 'data.diabetesRelative1'),
            column('diabetesRelative2', 'data.diabetesRelative2'),
            column('diabetesRelative3', 'data.diabetesRelative3'),
        ]
        self._columns.extend(get_meta_columns(self.config))
        q = queries.get_form_data(self.config)
        self._query = q


@register('ipos')
class IposExporter(Exporter):
    def run(self):
        self._columns = [
            column('id'),
            column('patient_id'),
            column('date', 'data.date'),
            column('score1', 'data.score1'),
            column('score2', 'data.score2'),
            column('score3', 'data.score3'),
            column('score4', 'data.score4'),
            column('score5', 'data.score5'),
            column('score6', 'data.score6'),
            column('score7', 'data.score7'),
            column('score8', 'data.score8'),
            column('score9', 'data.score9'),
            column('score10', 'data.score10'),
            column('score11', 'data.score11'),
            column('score12', 'data.score12'),
            column('score13', 'data.score13'),
            column('score14', 'data.score14'),
            column('score15', 'data.score15'),
            column('score16', 'data.score16'),
            column('score17', 'data.score17'),
            column('question1', 'data.question1'),
            column('score18', 'data.score18'),
            column('question2', 'data.question2'),
            column('score19', 'data.score19'),
            column('question3', 'data.question3'),
            column('score20', 'data.score20'),
            column('question4', 'data.question4'),
            column('question5', 'data.question5'),
            column('score', 'data.score'),
        ]
        self._columns.extend(get_meta_columns(self.config))
        q = queries.get_form_data(self.config)
        self._query = q


@register('samples')
class SamplesExporter(Exporter):
    def run(self):
        self._columns = [
            column('id'),
            column('patient_id'),
            column('date', 'taken_on'),
            column('barcode'),
            column('epa'),
            column('epb'),
            column('lpa'),
            column('lpb'),
            column('uc'),
            column('ub'),
            column('ud'),
            column('fub'),
            column('sc'),
            column('sa'),
            column('sb'),
            column('rna'),
            column('wb'),
            column('protocol_id'),
        ]
        self._columns.extend(get_meta_columns(self.config))
        q = queries.get_nurture_samples(self.config)
        self._query = q


@register('anthropometrics')
class AnthropometricsExporter(Exporter):
    def run(self):
        self._columns = [
            column('id'),
            column('patient_id'),
            column('date', 'data.date'),
            column('height', 'data.height'),
            column('weight', 'data.weight'),
            column('hip', 'data.hip'),
            column('waist', 'data.waist'),
            column('arm', 'data.arm'),
            column('up', 'data.up'),
            column('gripDominant', 'data.gripDominant'),
            column('gripNonDominant', 'data.gripNonDominant'),
            column('karnofsky', 'data.karnofsky'),
            column('systolic1', 'data.systolic1'),
            column('systolic2', 'data.systolic2'),
            column('systolic3', 'data.systolic3'),
            column('systolic', 'data.systolic'),
            column('diastolic1', 'data.diastolic1'),
            column('diastolic2', 'data.diastolic2'),
            column('diastolic3', 'data.diastolic3'),
            column('diastolic', 'data.diastolic'),
        ]
        self._columns.extend(get_meta_columns(self.config))
        q = queries.get_form_data(self.config)
        self._query = q


@register('socio-economic')
class SocioEconomicExporter(Exporter):
    def run(self):
        self._columns = [
            column('id'),
            column('patient_id'),
            column('maritalStatus', 'data.maritalStatus'),
            column('education', 'data.education'),
            column('employmentStatus', 'data.employmentStatus'),
            column('firstLanguage', 'data.firstLanguage'),
            column('literacy', 'data.literacy'),
            column('literacyHelp', 'data.literacyHelp'),
            column('smoking', 'data.smoking'),
            column('cigarettesPerDay', 'data.cigarettesPerDay'),
            column('alcohol', 'data.alcohol'),
            column('unitsPerWeek', 'data.unitsPerWeek'),
            column('diet', 'data.diet'),
            column('otherDiet', 'data.otherDiet'),
        ]
        self._columns.extend(get_meta_columns(self.config))
        q = queries.get_form_data(self.config)
        self._query = q


@register('nurtureckd')
class NurtureCKDExporter(Exporter):
    def run(self):
        self._columns = [
            column('id'),
            column('patient_id'),
            column('date', 'data.date'),
            column('visit', 'data.visit'),
            column('vaccinationFlu', 'data.vaccinationFlu'),
            column('vaccinationPneumonia', 'data.vaccinationPneumonia'),
            column('admission', 'data.admission'),
            column('admissionNumber', 'data.admissionNumber'),
            column('admissionEmergency', 'data.admissionEmergency'),
            column('admissionPlanned', 'data.admissionPlanned'),
            column('admissionDays', 'data.admissionDays'),
            column('admissionAntibiotics', 'data.admissionAntibiotics'),
            column('medicine1', 'data.medicine1'),
            column('tabletsParacetamol', 'data.tabletsParacetamol'),
            column('yearsParacetamol', 'data.yearsParacetamol'),
            column('medicine2', 'data.medicine2'),
            column('tabletsCocodamol', 'data.tabletsCocodamol'),
            column('yearsCocodamol', 'data.yearsCocodamol'),
            column('medicine3', 'data.medicine3'),
            column('tabletsIbuprofen', 'data.tabletsIbuprofen'),
            column('yearsIbuprofen', 'data.yearsIbuprofen'),

        ]
        self._columns.extend(get_meta_columns(self.config))
        q = queries.get_form_data(self.config)
        self._query = q


@register('renal_imaging')
class RenalImagingExporter(Exporter):
    def run(self):
        self._columns = [
            column('id'),
            column('patient_id'),
            column('source_group_id'),
            column('source_group', 'source_group.name'),
            column('source_type'),
            column('date', lambda x: format_date(x.date)),
            column('imaging_type'),
            column('right_present'),
            column('right_type'),
            column('right_length'),
            column('right_volume'),
            column('right_cysts'),
            column('right_stones'),
            column('right_calcification'),
            column('right_nephrocalcinosis'),
            column('right_nephrolithiasis'),
            column('right_other_malformation'),
            column('left_present'),
            column('left_type'),
            column('left_length'),
            column('left_volume'),
            column('left_cysts'),
            column('left_stones'),
            column('left_calcification'),
            column('left_nephrocalcinosis'),
            column('left_nephrolithiasis'),
            column('left_other_malformation'),
        ]

        self._columns.extend(get_meta_columns(self.config))

        q = queries.get_renal_imaging(self.config)
        self._query = q


@register('consultants')
class ConsultantsExporter(Exporter):
    def run(self):
        self._columns = [
            column('id'),
            column('first_name'),
            column('last_name'),
            column('email'),
            column('telephone_number'),
            column('gmc_number'),
            column('specialty', 'specialty.name')
        ]
        q = queries.get_consultants(self.config)
        self._query = q


@register('pregnancies')
class PregnanciesExporter(Exporter):
    def run(self):
        self._columns = [
            column('id'),
            column('patient_id'),
            column('pregnancy_number'),
            column('date_of_lmp', lambda x: format_date(x.date_of_lmp)),
            column('gravidity'),
            column('parity1'),
            column('parity2'),
            column('outcome'),
            column('weight'),
            column('weight_centile'),
            column('gestational_age'),
            column('delivery_method'),
            column('neonatal_intensive_care'),
            column('pre_eclampsia'),
        ]

        self._columns.extend(get_meta_columns(self.config))

        q = queries.get_pregnancies(self.config)
        self._query = q


@register('fetal_ultrasounds')
class FetalUltrasoundsExporter(Exporter):
    def run(self):
        self._columns = [
            column('id'),
            column('patient_id'),
            column('source_group_id'),
            column('source_group', 'source_group.name'),
            column('source_type'),
            column('date_of_scan', lambda x: format_date(x.date_of_scan)),
            column('fetal_identifier'),
            column('gestational_age'),
            column('head_centile'),
            column('abdomen_centile'),
            column('uterine_artery_notched'),
            column('liquor_volume'),
            column('comments'),
        ]

        self._columns.extend(get_meta_columns(self.config))

        q = queries.get_fetal_ultrasounds(self.config)
        self._query = q


@register('clinical_features')
class ClinicalFeaturesExporter(Exporter):
    def run(self):
        self._columns = [
            column('id'),
            column('patient_id'),
            column('normal_pregnancy'),
            column('abnormal_pregnancy_text'),
            column('neurological_problems'),
            column('seizures'),
            column('abnormal_gait'),
            column('deafness'),
            column('other_neurological_problem'),
            column('other_neurological_problem_text'),
            column('joint_problems'),
            column('joint_problems_age'),
            column('x_ray_abnormalities'),
            column('chondrocalcinosis'),
            column('other_x_ray_abnormality'),
            column('other_x_ray_abnormality_text'),
        ]

        self._columns.extend(get_meta_columns(self.config))
        q = queries.get_clinical_features(self.config)
        self._query = q


@register('liver-imaging')
class LiverImagingExporter(Exporter):
    def run(self):
        self._columns = [
            column('id'),
            column('patient_id'),
            column('source_group', 'source_group.name'),
            column('source_type'),
            column('date', lambda x: format_date(x.date)),
            column('imaging_type'),
            column('size'),
            column('hepatic_fibrosis'),
            column('hepatic_cysts'),
            column('bile_duct_cysts'),
            column('dilated_bile_ducts'),
            column('cholangitis'),
        ]
        q = queries.get_liver_imaging(self.config)
        self._query = q


@register('liver-diseases')
class LiverDiseasesExporter(Exporter):
    def run(self):
        self._columns = [
            column('id'),
            column('patient_id'),
            column('portal_hypertension'),
            column('portal_hypertension_date'),
            column('ascites'),
            column('ascites_date', lambda x: format_date(x.ascites_date)),
            column('oesophageal'),
            column('oesophageal_date', lambda x: format_date(x.oesophageal_date)),
            column('oesophageal_bleeding'),
            column('oesophageal_bleeding_date', lambda x: format_date(x.oesophageal_bleeding_date)),
            column('gastric'),
            column('gastric_date', lambda x: format_date(x.gastric_date)),
            column('gastric_bleeding'),
            column('gastric_bleeding_date', lambda x: format_date(x.gastric_bleeding_date)),
            column('anorectal'),
            column('anorectal_date', lambda x: format_date(x.anorectal_date)),
            column('anorectal_bleeding'),
            column('anorectal_bleeding_date', lambda x: format_date(x.anorectal_bleeding_date)),
            column('cholangitis_acute'),
            column('cholangitis_acute_date', lambda x: format_date(x.cholangitis_acute_date)),
            column('cholangitis_recurrent'),
            column('cholangitis_recurrent_date', lambda x: format_date(x.cholangitis_recurrent_date)),
            column('spleen_palpable'),
            column('spleen_palpable_date', lambda x: format_date(x.spleen_palpable_date)),
        ]
        q = queries.get_liver_diseases(self.config)
        self._query = q


@register('liver-transplants')
class LiverTransplantsExporter(Exporter):
    def run(self):
        self._columns = [
            column('id'),
            column('patient_id'),
            column('source_group', 'source_group.name'),
            column('source_type'),
            column('transplant_group', 'transplant_group.name'),
            column('registration_date', lambda x: format_date(x.registration_date)),
            column('transplant_date', lambda x: format_date(x.transplant_date)),
            column('indications'),
            column('other_indications'),
            column('first_graft_source'),
            column('loss_reason'),
            column('other_loss_reason'),
        ]
        q = queries.get_liver_transplants(self.config)
        self._query = q


@register('nephrectomies')
class NephrectomiesExporter(Exporter):
    def run(self):
        self._columns = [
            column('id'),
            column('patient_id'),
            column('source_group', 'source_group.name'),
            column('source_type'),
            column('date', lambda x: format_date(x.date)),
            column('kidney_side'),
            column('kidney_type'),
            column('entry_type'),
        ]
        q = queries.get_nephrectomies(self.config)
        self._query = q


@register('nutrition')
class NutritionExporter(Exporter):
    def run(self):
        self._columns = [
            column('id'),
            column('patient_id'),
            column('source_group', 'source_group.name'),
            column('source_type'),
            column('feeding_type'),
            column('from_date', lambda x: format_date(x.from_date)),
            column('to_date', lambda x: format_date(x.to_date)),
        ]
        q = queries.get_nutrition(self.config)
        self._query = q


@register('consents')
class ConsentsExporter(Exporter):
    def run(self):
        self._columns = [
            column('id'),
            column('patient_id'),
            column('consent', 'consent.label'),
            column('signed_on_date', lambda x: format_date(x.signed_on_date)),
        ]
        q = queries.get_consents(self.config)
        self._query = q


@register('alport-clinical-pictures')
class AlportPicturesExporter(Exporter):
    def run(self):
        self._columns = [
            column('id'),
            column('patient_id'),
            column('date_of_picture', lambda x: format_date(x.date_of_picture)),
            column('deafness'),
            column('deafness_date', lambda x: format_date(x.deafness_date)),
            column('hearing_aid_date', lambda x: format_date(x.hearing_aid_date)),

        ]
        self._columns.extend(get_meta_columns(self.config))
        q = queries.get_alport_clinical_pictures(self.config)
        self._query = q


@register('rituximab-criteria')
class RituximabConsentsExporter(Exporter):
    def run(self):
        self._columns = [
            column('id'),
            column('patient_id'),
            column('date', lambda x: format_date(x.date)),
            column('therapy_failure'),
            column('hypersensitivity'),
            column('drug_associated_toxicity'),
            column('alkylating_complication'),
            column('alkylating_failure_monitoring_requirements'),
            column('cancer'),
            column('threatened_fertility'),
            column('fall_in_egfr'),
            column('cni_therapy_complication'),
            column('cni_failure_monitoring_requirements'),
            column('diabetes'),
            column('risk_factors'),
        ]
        self._columns.extend(get_meta_columns(self.config))
        q = queries.get_rituximab_consents(self.config)
        self._query = q


@register('rituximab-visits')
class RituximabVisitsExporter(Exporter):
    def run(self):
        self._columns = [
            column('id'),
            column('patient_id'),
            column('date', 'data.date'),
            column('label', 'data.visit'),
        ]
        self._columns.extend(get_meta_columns(self.config))
        q = queries.get_form_data(self.config)
        self._query = q


@register('rituximab-baseline-assessment')
class RituximabBaselineAssessmentExporter(Exporter):
    def run(self):
        self._columns = [
            column('id'),
            column('patient_id'),
            column('source_group', 'source_group.name'),
            column('date'),
            column('nephropathy'),
        ]
        q = queries.get_rituximab_baseline_assessment_data(self.config)
        self._query = q

    @property
    def dataset(self):
        self._columns.extend(column(item.lower()) for item in SUPPORTIVE_MEDICATIONS.keys())
        previous = (
            'chlorambucil',
            'cyclophosphamide',
            'rituximab',
            'tacrolimus',
            'cyclosporine',
        )

        with_dose = ('chlorambucil', 'cyclophosphamide', 'rituximab')
        for item in previous:
            items = (item, '{}_start_date'.format(item), '{}_end_date'.format(item))
            self._columns.extend(column(item) for item in items)
            if item in with_dose:
                self._columns.append(column('{}_dose'.format(item)))

        self._columns.append(column('steroids'))
        self._columns.append(column('other_previous_treatment'))
        self._columns.append(column('past_remission'))
        self._columns.append(column('performance_status'))
        self._columns.extend(get_meta_columns(self.config))
        dataset = make_dataset(self._columns)

        for entry in self._query:
            row = [entry.id, entry.patient_id, entry.source_group.name, entry.date, entry.nephropathy]
            for item in SUPPORTIVE_MEDICATIONS.keys():
                row.append(entry.supportive_medication.count(item) != 0)
            for item in previous:
                if not entry.previous_treatment:
                    present = {}
                else:
                    present = entry.previous_treatment.get(item, {})

                if present.get(item, False):
                    row.append(present.get(item))
                    row.append(present.get('start_date', ''))
                    row.append(present.get('end_date', ''))
                else:
                    row.append(False)
                    row.append('')
                    row.append('')

                if item in with_dose:
                    row.append(present.get('total_dose', 'False'))

            row.append(entry.steroids)
            row.append(entry.other_previous_treatment)
            row.append(entry.past_remission)
            row.append(entry.performance_status)

            for col in self._columns[-6:]:
                row.append(col[1](entry))

            dataset.append(row)
        return dataset


@register('rituximab-administration')
class RituximabAdministrationExporter(Exporter):
    def run(self):
        self._columns = [
            column('id'),
            column('patient_id'),
            column('date', 'data.date'),
            column('drug_name', 'data.drugName'),
            column('other_drug', 'data.otherDrug'),
            column('dose', 'data.dose'),
            column('retreatment', 'data.retreatment'),
            column('toxicity', stringify_list('toxicity')),
            column('other_toxicity', 'data.otherToxicity'),
        ]

        self._columns.extend(get_meta_columns(self.config))
        q = queries.get_form_data(self.config)
        self._query = q


@register('rituximab-assessment')
class RituximabFollowupAssessmentExporter(Exporter):
    def run(self):
        self._columns = [
            column('id'),
            column('patient_id'),
            column('date', 'data.date'),
            column('visit', 'data.visit'),
            column('performance', 'data.performance'),
            column('transplant', 'data.transplant'),
            column('haemodialysis', 'data.haemodialysis'),
            column('peritoneal_dialysis', 'data.peritonealDialysis'),
            column('supportive_medication', stringify_list('medication'))
        ]
        self._columns.extend(get_meta_columns(self.config))
        q = queries.get_form_data(self.config)
        self._query = q


@register('rituximab-adverse-events')
class RituximabAdverseEventsExporter(Exporter):
    def run(self):
        self._columns = [
            column('id'),
            column('patient_id'),
            column('date', 'data.date'),
            column('hospitalisation', 'data.hospitalisation'),
            column('adverse_events', 'data.adverseEvents'),
            column('onset_cancer', 'data.newOnsetCancer'),
            column('thromboembolism', 'data.thromboembolism'),
            column('myocardial_infarction', 'data.myocardialInfarction'),
            column('stroke', 'data.stroke'),
            column('ischaemic_attack', 'data.ischaemicAttack'),
            column('other_adverse_event', 'data.otherAdverseEvent'),
            column('other_toxicity', 'data.otherTox'),
            column('date_of_death', 'data.dod'),
            column('cause_of_death', 'data.dodCause')
        ]
        self._columns.extend(get_meta_columns(self.config))
        q = queries.get_form_data(self.config)
        self._query = q


@register('adtkd-clinical-pictures')
class ADTKDClinicalPicturesExporter(Exporter):
    def run(self):
        self._columns = [
            column('id'),
            column('patient_id'),
            column('picture_date'),
            column('gout'),
            column('gout_date'),
            column('family_gout'),
            column('family_gout_relatives'),
            column('thp'),
            column('uti'),
            column('comments')
        ]
        self._columns.extend(get_meta_columns(self.config))
        q = queries.get_adtkd_clinical_pictures(self.config)
        self._query = q
