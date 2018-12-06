"""
Script to do simple validations on nurture export.
"""

from collections import defaultdict, OrderedDict
import datetime
import itertools

from sqlalchemy import text
import xlsxwriter

from radar.app import Radar
from radar.database import db
from radar.exporter.utils import get_months, get_years
from radar.models.diagnoses import GROUP_DIAGNOSIS_TYPE
from radar.models.groups import Group


try:
    basestring
except NameError:
    basestring = str

DATEFMT = '%d/%m/%Y'
DATETIMEFMT = '%d/%m/%Y %H:%M:%S'
BLOOD_PRESSURE_DELTA = 10
DAYS_RESULTS_SHOULD_BE_WITHIN = 7


class SheetWrapper(object):
    """Class keeping track on which line it has written row."""

    def __init__(self, sheet):
        self.sheet = sheet
        self.current_line = 0
        self.first_line = True

    def write_row(self, data, format=None):
        """Write row to a sheet and keep track position."""
        if self.first_line:
            self.first_line = False
        else:
            self.current_line = self.current_line + 1

        self.sheet.write_row(self.current_line, 0, data, format)

    def write(self, col, data, format=None):
        """Write a single cell."""
        self.sheet.write(self.current_line, col, data, format)


def get_gender(gender_code):
    genders = {0: 'NA', 1: 'M', 2: 'F', 9: 'Not specified'}
    return genders.get(gender_code, 'NA')


def format_date(date, long=False):
    if date and isinstance(date, basestring):
        return date
    try:
        if date and long:
            return date.strftime(DATETIMEFMT)
        elif date:
            return date.strftime(DATEFMT)
    except ValueError:
        datestr = date.isoformat().split("T")[0].split('-')
        return '/'.join(datestr[::-1])
    return None


def get_form_data(entry, bounds, fields):
    data = [entry.patient_id]
    for field in fields[bounds]:
        data.append(entry.data.get(field, None))

    data.append(format_date(entry.created_date))
    data.append(entry.created_user.name)
    data.append(format_date(entry.modified_date))
    data.append(entry.modified_user.name)
    return data


def in_date_range(visit_date, test_date, days=DAYS_RESULTS_SHOULD_BE_WITHIN):
    margin = datetime.timedelta(days=days)
    return test_date - margin <= visit_date <= test_date + margin


class BaseSheet(object):
    def is_value_missing(self, prop):
        return bool(getattr(self, prop))

    @property
    def header(self):
        return self.fields

    def __iter__(self):
        return self

    def __next__(self):
        if self.current_field < len(self.fields):
            self.current_field += 1
            try:
                value = getattr(self, self.fields[self.current_field - 1])
            except AttributeError:
                value = getattr(self.original_obj, self.fields[self.current_field - 1])
            return value if value is not None else ''

        raise StopIteration

    next = __next__


class Basic(BaseSheet):
    __sheetname__ = 'patients'

    def __init__(self, patient, group):
        self.original_obj = patient
        self.patient_id = patient.id
        self.patient_number = patient.primary_patient_number_number
        self.ethnicity = patient.ethnicity.label if patient.ethnicity else None
        self.pv_link = True if patient.ukrdc else False
        self.control = True if patient.control else False
        self.gender = get_gender(patient.gender)
        self.date_of_birth = format_date(patient.date_of_birth)
        self.date_of_death = format_date(patient.date_of_death)
        self.recruited_date = format_date(patient.recruited_date(group))
        self.recruited_group = group.code
        self.recruited_user = patient.recruited_user(group).name

        self.current_field = 0
        self.fields = (
            'patient_id',
            # 'nurture_ins',
            # 'nurture_ckd',
            'patient_number',
            'first_name',
            'last_name',
            'date_of_birth',
            'date_of_death',
            'gender',
            'ethnicity',
            'pv_link',
            # 'control',
            'recruited_date',
            'recruited_group',
            'recruited_user',
        )

    def export(self, sheet, errorfmt=None, warningfmt=None):
        sheet.write_row(self)
        if not self.ethnicity:
            sheet.write(7, '', errorfmt)
        if not self.pv_link:
            sheet.write(8, '', errorfmt)


class Comorbidities(BaseSheet):
    __sheetname__ = 'comorbidities'

    def __init__(self, patient, diagnoses, primary_diagnoses):
        self.patient = patient
        self.diagnoses = diagnoses
        self.primary_diagnoses = primary_diagnoses
        self.fields = (
            'patient_id',
            'source_group',
            'source_type',
            'diagnosis',
            'diagnosis_text',
            'symptoms_date',
            'symptoms_age_years',
            'symptoms_age_months',
            'from_date',
            'from_age_years',
            'from_age_months',
            'to_date',
            'to_age_years',
            'to_age_months',
            'gene_test',
            'biochemistry',
            'clinical_picture',
            'biopsy',
            'biopsy_diagnosis',
            'biopsy_diagnosis_label',
            'comments',
            'created_date',
            'created_user',
            'modified_date',
            'modified_user',
        )

    def export(self, sheet, errorfmt=None, warningfmt=None):
        recorded = False
        for diagnosis in self.diagnoses:
            if diagnosis.diagnosis in self.primary_diagnoses:
                continue
            recorded = True
            data = [getattr(diagnosis, field) for field in self.fields if hasattr(diagnosis, field)]

            data[1] = diagnosis.source_group.code

            data[3] = data[3].name if data[3] else None

            data[5] = format_date(data[5])
            data.insert(6, get_years(diagnosis.symptoms_age))
            data.insert(7, get_months(diagnosis.symptoms_age))

            data[8] = format_date(data[8])
            data.insert(9, get_years(diagnosis.from_age))
            data.insert(10, get_months(diagnosis.from_age))

            data[11] = format_date(data[11])
            data.insert(12, get_years(diagnosis.to_age))
            data.insert(13, get_months(diagnosis.to_age))

            data[-4] = format_date(data[-4])
            data[-3] = diagnosis.created_user.name
            data[-2] = format_date(data[-2])
            data[-1] = diagnosis.modified_user.name

            sheet.write_row(data)
        if not recorded:
            sheet.write_row([self.patient.id, '', '', 'NO COMORBIDITIES RECORDED'], errorfmt)


class Diagnoses(BaseSheet):
    __sheetname__ = 'primary_diagnoses'

    def __init__(self, patient, diagnoses, primary_diagnoses):
        self.patient = patient
        self.diagnoses = diagnoses
        self.primary_diagnoses = primary_diagnoses
        self.fields = (
            'patient_id',
            'source_group',
            'source_type',
            'edta_code',
            'diagnosis',
            'diagnosis_text',
            'symptoms_date',
            'symptoms_age_years',
            'symptoms_age_months',
            'from_date',
            'from_age_years',
            'from_age_months',
            'to_date',
            'to_age_years',
            'to_age_months',
            'gene_test',
            'biochemistry',
            'clinical_picture',
            'biopsy',
            'biopsy_diagnosis',
            'biopsy_diagnosis_label',
            'comments',
            'created_date',
            'created_user',
            'modified_date',
            'modified_user',
        )

    def export(self, sheet, errorfmt=None, warningfmt=None):
        recorded = False
        for diagnosis in self.diagnoses:
            if diagnosis.diagnosis not in self.primary_diagnoses:
                continue
            recorded = True
            data = [getattr(diagnosis, field) for field in self.fields if hasattr(diagnosis, field)]

            data[1] = diagnosis.source_group.code

            if diagnosis.diagnosis and diagnosis.diagnosis.codes:
                for code in diagnosis.diagnosis.codes:
                    if code.system == 'ERA-EDTA PRD':
                        data.insert(3, code.code)
                        break
                else:
                    data.insert(3, None)

            data[4] = data[4].name if data[4] else None

            data[6] = format_date(data[6])
            data.insert(7, get_years(diagnosis.symptoms_age))
            data.insert(8, get_months(diagnosis.symptoms_age))

            data[9] = format_date(data[9])
            data.insert(10, get_years(diagnosis.from_age))
            data.insert(11, get_months(diagnosis.from_age))

            data[12] = format_date(data[12])
            data.insert(13, get_years(diagnosis.to_age))
            data.insert(14, get_months(diagnosis.to_age))

            data[-4] = format_date(data[-4])
            data[-3] = diagnosis.created_user.name
            data[-2] = format_date(data[-2])
            data[-1] = diagnosis.modified_user.name

            sheet.write_row(data)
        if not recorded:
            sheet.write_row([self.patient.id, '', '', 'MISSING DIAGNOSIS'], errorfmt)


class SocioEconomic(BaseSheet):
    __sheetname__ = 'socio-economic'

    def __init__(self, patient):
        self.patient = patient
        self.fields = (
            'patient_id',
            'maritalStatus',
            'education',
            'employmentStatus',
            'firstLanguage',
            'literacy',
            'literacyHelp',
            'smoking',
            'cigarettesPerDay',
            'alcohol',
            'unitsPerWeek',
            'diet',
            'otherDiet',
            'created_date',
            'created_user',
            'modified_date',
            'modified_user',
        )

    def export(self, sheet, errorfmt, warningfmt):
        entries = [entry for entry in self.patient.entries if entry.form.slug == 'socio-economic']
        if entries:
            for entry in entries:
                data = get_form_data(entry, slice(1, -4), self.fields)
                sheet.write_row(data)
                for col in (1, 2, 3, 4, 5, 6, 7, 9):
                    if data[col] is None:
                        sheet.write(col, '', errorfmt)
                if data[7] and data[8] is None:
                    sheet.write(8, '', warningfmt)
                if data[9] and data[10] is None:
                    sheet.write(10, '', warningfmt)
        else:
            sheet.write_row([self.patient.id], errorfmt)


class NurtureCKD(BaseSheet):
    __sheetname__ = 'visits'

    def __init__(self, patient):
        self.patient = patient
        self.fields = (
            'patient_id',
            'date',
            'visit',
            'vaccinationFlu',
            'vaccinationPneumonia',
            'admission',
            'admissionNumber',
            'admissionEmergency',
            'admissionPlanned',
            'admissionDays',
            'admissionAntibiotics',
            'medicine1',
            'tabletsParacetamol',
            'yearsParacetamol',
            'medicine2',
            'tabletsCocodamol',
            'yearsCocodamol',
            'medicine3',
            'tabletsIbuprofen',
            'yearsIbuprofen',
            'created_date',
            'created_user',
            'modified_date',
            'modified_user',
        )

    def export(self, sheet, errorfmt, warningfmt):
        # everything is validated on form submit, technically it is impossible
        # to have missing fields
        entries = [entry for entry in self.patient.entries if entry.form.slug == 'nurtureckd']
        if entries:
            for entry in entries:
                data = get_form_data(entry, slice(1, -4), self.fields)
                sheet.write_row(data)
        else:
            sheet.write_row([self.patient.id], errorfmt)


class FamilyDiseasesHistory(BaseSheet):
    __sheetname__ = 'family-diseases-history'

    def __init__(self, patient):
        self.patient = patient
        self.fields = (
            'patient_id',
            'chd',
            'eskd',
            'diabetes',
            'chdRelative1',
            'chdRelative2',
            'chdRelative3',
            'eskdRelative1',
            'eskdRelative2',
            'eskdRelative3',
            'diabetesRelative1',
            'diabetesRelative2',
            'diabetesRelative3',
            'created_date',
            'created_user',
            'modified_date',
            'modified_user',
        )

    def export(self, sheet, errorfmt, warningfmt):
        entries = [entry for entry in self.patient.entries if entry.form.slug == 'family-history']
        if entries:
            for entry in entries:
                data = get_form_data(entry, slice(1, -4), self.fields)
                sheet.write_row(data)
        else:
            sheet.write_row([self.patient.id], errorfmt)


class DiabeticComplications(BaseSheet):
    __sheetname__ = 'diabetic-complications'

    def __init__(self, patient):
        self.patient = patient
        self.fields = (
            'patient_id',
            'laser',
            'foot',
            'ulcers',
            'retinopathy',
            'peripheral',
            'neuropathy',
            'created_date',
            'created_user',
            'modified_date',
            'modified_user',
        )

    def export(self, sheet, errorfmt, warningfmt):
        entries = [entry for entry in self.patient.entries if entry.form.slug == 'diabetic-complications']
        diagnoses = [diagnosis for diagnosis in self.patient.patient_diagnoses if diagnosis.status]
        interested = set(('Diabetes - Type I', 'Diabetes - Type II', 'Diabetes'))
        diabetes = [diagnosis for diagnosis in diagnoses if diagnosis.name in interested]
        if diabetes and not entries:
            sheet.write_row([self.patient.id], errorfmt)

        if entries:
            for entry in entries:
                data = get_form_data(entry, slice(1, -4), self.fields)
                sheet.write_row(data)


def in_range(values):
    for first, second in itertools.combinations(values, 2):
        if first is None or second is None:
            return False
        if abs(first - second) > BLOOD_PRESSURE_DELTA:
            return False
    return True


class Anthropometrics(BaseSheet):
    __sheetname__ = 'anthropometrics'

    def __init__(self, patient):
        self.patient = patient
        self.fields = (
            'patient_id',
            'date',
            'height',
            'weight',
            'hip',
            'waist',
            'arm',
            'up',
            'grip',
            'karnofsky',
            'systolic1',
            'systolic2',
            'systolic3',
            'systolic',
            'diastolic1',
            'diastolic2',
            'diastolic3',
            'diastolic',
            'created_date',
            'created_user',
            'modified_date',
            'modified_user',
        )

    def export(self, sheet, errorfmt, warningfmt):
        entries = [entry for entry in self.patient.entries if entry.form.slug == 'anthropometrics']
        if entries:
            for entry in entries:

                data = get_form_data(entry, slice(1, -4), self.fields)
                sheet.write_row(data)

                for no, item in enumerate(data):
                    if not item:
                        sheet.write(no, data[no], errorfmt)

                if not in_range(data[10:13]):
                    sheet.write(10, data[10], errorfmt)
                    sheet.write(11, data[11], errorfmt)
                    sheet.write(12, data[12], errorfmt)

                if not in_range(data[14:17]):
                    sheet.write(14, data[14], errorfmt)
                    sheet.write(15, data[15], errorfmt)
                    sheet.write(16, data[16], errorfmt)

        else:
            sheet.write_row([self.patient.id], errorfmt)


class Medications(BaseSheet):
    __sheetname__ = 'medications'

    def __init__(self, patient):
        self.patient = patient
        self.fields = (
            'patient_id',
            'source_group',
            'source_type',
            'from_date',
            'to_date',
            'drug_id',
            'drug',
            'drug_text',
            'dose_quantity',
            'dose_unit',
            'dose_unit_label',
            'dose_text',
            'frequency',
            'route',
            'route_label',
            'created_date',
            'created_user',
            'modified_date',
            'modified_user',
        )

    def export(self, sheet, errorfmt=None, warningfmt=None):
        medications = self.patient.medications
        if medications:
            for instance in medications:
                data = [getattr(instance, field) for field in self.fields]
                data[1] = instance.source_group.code

                data[3] = format_date(data[3])
                data[4] = format_date(data[4])
                data[6] = instance.drug.name if (instance.drug) else None

                data[-4] = format_date(data[-4])
                data[-3] = instance.created_user.name
                data[-2] = format_date(data[-2])
                data[-1] = instance.modified_user.name

                sheet.write_row(data)

                for i in (3, 8, 9, 12):
                    if not data[i]:
                        sheet.write(i, '', errorfmt)

                if not data[6] and not data[7]:
                    sheet.write(6, '', errorfmt)
                    sheet.write(7, '', errorfmt)

        else:
            sheet.write_row([self.patient.id], errorfmt)


class Results(BaseSheet):
    __sheetname__ = 'results'

    def __init__(self, patient, results, observations):
        self.patient = patient
        self.results = results
        self.observations = observations
        self.fields = ['patient_id', 'source_group', 'source_type', 'date']
        self.fields.extend(self.observations)

    def export(self, sheet, errorfmt=None, warningfmt=None):
        data = OrderedDict()
        visit_dates = [i.data.get('date') for i in self.patient.entries if i.form.slug == 'nurtureckd']

        within_range = False
        for result in self.results:
            datestr = result.date.strftime(DATETIMEFMT)
            key = (result.patient_id, result.source_group.name, result.source_type, datestr)
            if key not in data:
                data[key] = {}

            data[key][result.observation.name] = result.value_label_or_value

            for visit in visit_dates:
                visit_date = datetime.datetime.strptime(visit, '%Y-%m-%d')
                if not within_range and in_date_range(visit_date, result.date.replace(tzinfo=None)):
                    within_range = True

        if not within_range:
            msg = 'NO RESULTS WITHIN {} DAYS OF VISIT'.format(DAYS_RESULTS_SHOULD_BE_WITHIN)
            sheet.write_row([self.patient.id, msg], errorfmt)

        for key, results in data.items():
            data = list(key)
            for test in self.observations:
                data.append(results.get(test, None))

            sheet.write_row(data)


class Pathology(BaseSheet):
    __sheetname__ = 'pathology'

    def __init__(self, patient):
        self.patient = patient
        self.fields = (
            'patient_id',
            'source_group',
            'date',
            'kidney_type',
            'kidney_type_label',
            'kidney_side',
            'kidney_side_label',
            'reference_number',
            'image_url',
            'histological_summary',
            'em_findings',
            'created_date',
            'created_user',
            'modified_date',
            'modified_user',
        )

    def export(self, sheet, errorfmt=None, warningfmt=None):
        visit_dates = [i.data.get('date') for i in self.patient.entries if i.form.slug == 'nurtureckd']
        visit_dates = [datetime.datetime.strptime(i, '%Y-%m-%d').date() for i in visit_dates]

        # TODO: clean this stuff up.
        def within_date_range(pathology_date, test_date, days_before=182, days_after=14):
            margin_before = datetime.timedelta(days=days_before)
            margin_after = datetime.timedelta(days=days_after)
            return pathology_date >= test_date - margin_before and test_date + margin_after >= pathology_date

        pathologies = self.patient.pathology
        if pathologies:
            for instance in pathologies:
                data = [getattr(instance, field) for field in self.fields]
                data[1] = instance.source_group.code

                pathology_date = data[2]
                in_range = False
                for visit in visit_dates:
                    if within_date_range(pathology_date, visit):
                        in_range = True
                        break

                data[2] = format_date(pathology_date)
                data[-4] = format_date(data[-4])
                data[-3] = instance.created_user.name
                data[-2] = format_date(data[-2])
                data[-1] = instance.modified_user.name

                sheet.write_row(data)
                if not in_range:
                    sheet.write(2, format_date(pathology_date), errorfmt)
        else:
            sheet.write_row([self.patient.id], errorfmt)


class RenalProgressions(BaseSheet):
    __sheetname__ = 'renal_progressions'

    def __init__(self, patient):
        self.patient = patient
        self.fields = (
            'patient_id',
            'onset_date',
            'ckd3a_date',
            'ckd3b_date',
            'ckd4_date',
            'ckd5_date',
            'esrf_date',
            'created_date',
            'created_user',
            'modified_date',
            'modified_user',
        )

    def export(self, sheet, errorfmt=None, warningfmt=None):
        progressions = self.patient.renal_progressions
        if progressions:
            for instance in progressions:
                data = [getattr(instance, field) for field in self.fields]
                data[1] = format_date(data[1])
                data[2] = format_date(data[2])
                data[3] = format_date(data[3])
                data[4] = format_date(data[4])
                data[5] = format_date(data[5])
                data[6] = format_date(data[6])

                data[-4] = format_date(data[-4])
                data[-3] = instance.created_user.name
                data[-2] = format_date(data[-2])
                data[-1] = instance.modified_user.name

                sheet.write_row(data)

                if not data[1]:
                    sheet.write(1, '', errorfmt)

                if not any(data[2:6]):
                    for i in range(2, 6):
                        sheet.write(i, '', errorfmt)

        else:
            sheet.write_row([self.patient.id], errorfmt)


class Samples(BaseSheet):
    __sheetname__ = 'samples'

    def __init__(self, patient):
        self.patient = patient
        self.fields = (
            'patient_id',
            'date',
            'barcode',
            'created_date',
            'created_user',
            'modified_date',
            'modified_user',
        )

    def export(self, sheet, errorfmt, warningfmt):
        entries = [entry for entry in self.patient.entries if entry.form.slug == 'samples']
        if entries:
            for entry in entries:
                data = get_form_data(entry, slice(1, -4), self.fields)

                # data = [getattr(entry, field) for field in self.fields]
                # data[1] = format_date(data[1])
                # data[-4] = format_date(data[-4], long=True)
                # data[-3] = entry.created_user.name
                # data[-2] = format_date(data[-2], long=True)
                # data[-1] = entry.modified_user.name

                sheet.write_row(data)
        else:
            sheet.write_row([self.patient.id], errorfmt)


class Patient(object):
    __sheets__ = (
        'basic',
        'diagnoses',
        'comorbidities',
        'socioeconomic',
        'nurtureckd',
        'family_diseases_history',
        'diabetic_complications',
        'anthropometrics',
        'medications',
        'results',
        'pathology',
        'renal_progressions',
        'samples',
    )

    def __init__(self, patient, primary_diagnoses, group):
        self.primary_diagnoses = primary_diagnoses
        self.group = group
        self.original_patient = patient
        self.patient_id = patient.id
        self.basic = None
        self.diagnoses = None
        self.comorbidities = None
        self.socioeconomic = None
        self.nurtureckd = None
        self.family_diseases_history = None
        self.diabetic_complications = None
        self.anthropometrics = None
        self.medications = None
        self.results = None
        self.pathology = None
        self.renal_progressions = None
        self.samples = None

    def run(self):
        self.basic = Basic(self.original_patient, self.group)
        self.diagnoses = Diagnoses(
            self.original_patient,
            self.original_patient.patient_diagnoses,
            self.primary_diagnoses,
        )
        self.comorbidities = Comorbidities(
            self.original_patient,
            self.original_patient.patient_diagnoses,
            self.primary_diagnoses,
        )

        self.socioeconomic = SocioEconomic(self.original_patient)
        self.nurtureckd = NurtureCKD(self.original_patient)
        self.family_diseases_history = FamilyDiseasesHistory(self.original_patient)
        self.diabetic_complications = DiabeticComplications(self.original_patient)
        self.anthropometrics = Anthropometrics(self.original_patient)
        self.medications = Medications(self.original_patient)
        self.results = Results(self.original_patient, self.original_patient.results, self.observations)
        self.pathology = Pathology(self.original_patient)
        self.renal_progressions = RenalProgressions(self.original_patient)
        self.samples = Samples(self.original_patient)

    def add_observations(self, observations):
        self.observations = observations


class PatientList(object):
    def __init__(self, hospital, primary_diagnoses, kind, group):
        self.data = []
        self.hospital = hospital
        self.observations = set()
        self.stats = defaultdict(int)
        self.primary_diagnoses = primary_diagnoses
        self.kind = kind
        self.group = group

    def append(self, patient):
        self.observations |= set([result.observation.name for result in patient.results])
        groups = [group.code for group in patient.groups]
        if 'NURTUREINS' in groups:
            self.stats['NURTUREINS'] += 1
        if 'NURTURECKD' in groups:
            self.stats['NURTURECKD'] += 1

        self.stats['TOTAL'] += 1

        self.stats['UKRDC'] += patient.ukrdc
        self.data.append(Patient(patient, self.primary_diagnoses, self.group))

    def export(self):
        try:
            patient = self.data[0]
        except IndexError:
            print('No {} patients found in {}'.format(self.kind.upper(), self.hospital.name))
            return

        workbook = xlsxwriter.Workbook(
            '{}_{}_export.xlsx'.format(self.hospital.name, self.kind), {'remove_timezone': True})
        errorfmt = workbook.add_format({'bg_color': 'red'})
        warningfmt = workbook.add_format({'bg_color': 'orange'})

        summary_sheet = workbook.add_worksheet('Summary')
        summary_sheet.write('A1', 'Validation report')
        summary_sheet.write('B1', datetime.date.today().strftime('%Y-%m-%d'))
        summary_sheet.write('A3', 'Renal Unit')
        summary_sheet.write('B3', self.hospital.name)

        for patient in self.data:
            patient.add_observations(sorted(self.observations))
            patient.run()

        for attr in patient.__sheets__:
            obj = getattr(patient, attr)
            # sheet = workbook.add_worksheet(obj.__sheetname__)
            sheet = SheetWrapper(workbook.add_worksheet(obj.__sheetname__))
            sheet.write_row(obj.header)
            for patient in sorted(self.data, key=lambda pat: pat.patient_id):
                patient.run()
                patient.observations = sorted(self.observations)
                getattr(patient, attr).export(sheet, errorfmt, warningfmt)

        summary_sheet.write('A5', 'Total')
        summary_sheet.write('B5', self.stats.get('TOTAL', 0))

        summary_sheet.write('A7', 'Missing Patient View Link')
        summary_sheet.write('B7', self.stats.get('TOTAL', 0) - self.stats.get('UKRDC', 0))

        summary_sheet.write('A9', 'Patient list')
        summary_sheet.write('A10', 'Radar No')
        summary_sheet.write('B10', 'Patient Name')
        counter = itertools.count(11)
        for patient in self.data:
            col = next(counter)
            summary_sheet.write('A{}'.format(col), patient.patient_id)
            summary_sheet.write('B{}'.format(col), patient.original_patient.full_name)

        col = next(counter)
        col = next(counter)
        summary_sheet.write('A{}'.format(col), 'Missing PV link')
        col = next(counter)
        summary_sheet.write('A{}'.format(col), 'Radar No')
        summary_sheet.write('B{}'.format(col), 'Patient Name')
        for patient in self.data:
            if patient.original_patient.ukrdc:
                continue
            col = next(counter)
            summary_sheet.write('A{}'.format(col), patient.patient_id)
            summary_sheet.write('B{}'.format(col), patient.original_patient.full_name)


def get_hospitals():
    select_stmt = text('''
        SELECT DISTINCT created_group_id FROM group_patients
        WHERE group_id IN (
            SELECT id FROM groups
            WHERE code = 'NURTUREINS' OR code = 'NURTURECKD'
        )
    ''')
    results = db.session.execute(select_stmt)
    return [row for row, in results]


def export_validate():
    primary = GROUP_DIAGNOSIS_TYPE.PRIMARY

    nurtureins = Group.query.filter_by(code='NURTUREINS').first()
    nurtureins_primary_diagnoses = [
        diagnosis.diagnosis for diagnosis
        in nurtureins.group_diagnoses
        if diagnosis.type == primary
    ]

    nurtureckd = Group.query.filter_by(code='NURTURECKD').first()
    nurtureckd_primary_diagnoses = [
        diagnosis.diagnosis for diagnosis
        in nurtureckd.group_diagnoses
        if diagnosis.type == primary
    ]

    hospital_ids = get_hospitals()

    for hospital_id in hospital_ids:
        hospital = Group.query.get(hospital_id)

        ins_list = PatientList(hospital, nurtureins_primary_diagnoses, 'ins', nurtureins)
        ckd_list = PatientList(hospital, nurtureckd_primary_diagnoses, 'ckd', nurtureckd)
        for p in hospital.patients:
            if p.test or p.control:
                continue
            if p.in_group(nurtureckd):
                ckd_list.append(p)
            elif p.in_group(nurtureins):
                ins_list.append(p)
        ckd_list.export()
        ins_list.export()
        print(hospital_id)


def main():
    # argument_parser = argparse.ArgumentParser()
    # argument_parser.add_argument('config')
    # args = argument_parser.parse_args()

    app = Radar()

    # config_parser = ConfigParser.ConfigParser()
    # config_parser.readfp(open(args.config))
    with app.app_context():
        export_validate()


if __name__ == '__main__':
    main()
