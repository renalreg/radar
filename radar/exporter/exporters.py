import re

from radar.exporter import queries
from radar.exporter.utils import (
    format_date,
    format_user,
    get_months,
    get_years,
    identity_getter,
    none_getter,
    path_getter,
    stringify_list,
)
from radar.models.results import Observation
from radar.models.rituximab import SUPPORTIVE_MEDICATIONS
from radar.permissions import has_permission_for_patient
from radar.roles import PERMISSION
from radar.utils import get_attrs


ILLEGAL_CHARACTERS_RE = re.compile(r"[\000-\010]|[\013-\014]|[\016-\037]")

exporter_map = {}


def none_to_empty(value):
    return "" if value is None else value


def formatters(value):
    val = format_date(value)
    val = none_to_empty(val)
    return val


def register(name):
    """Add an exporter."""

    def decorator(cls):
        exporter_map[name] = cls
        return cls

    return decorator


def column(name, getter=None):
    if getter is None:
        getter = path_getter(name)
    elif isinstance(getter, str):
        getter = path_getter(getter)

    return name, getter


def demographics_column_factory(config):
    """Returns a column based on the config."""

    if config["anonymised"]:

        def column(name, getter=None, anonymised_getter=None, patient_getter=None):
            if anonymised_getter is None:
                anonymised_getter = none_getter
            elif isinstance(anonymised_getter, str):
                anonymised_getter = path_getter(anonymised_getter)

            return name, anonymised_getter

    elif config["user"] is not None:

        def column(name, getter=None, anonymised_getter=None, patient_getter=None):
            if getter is None:
                getter = path_getter(name)
            elif isinstance(getter, str):
                getter = path_getter(getter)

            if anonymised_getter is None:
                anonymised_getter = none_getter
            elif isinstance(anonymised_getter, str):
                anonymised_getter = path_getter(anonymised_getter)

            if patient_getter is None:
                patient_getter = path_getter("patient")
            elif isinstance(anonymised_getter, str):
                patient_getter = path_getter(patient_getter)

            def f(value):
                patient = patient_getter(value)

                if has_permission_for_patient(
                    config["user"], patient, PERMISSION.VIEW_DEMOGRAPHICS
                ):
                    return getter(value)
                else:
                    return anonymised_getter(value)

            return name, f

    else:

        def column(name, getter=None, anonymised_getter=None, patient_getter=None):
            if getter is None:
                getter = path_getter(name)
            elif isinstance(getter, str):
                getter = path_getter(getter)

            return name, getter

    return column


def get_meta_columns(config):
    def created_user(x):
        if config["anonymised"]:
            return ""
        return format_user(x.created_user)

    def modified_user(x):
        if config["anonymised"]:
            return ""
        return format_user(x.modified_user)

    return [
        column("created_date", lambda x: format_date(x.created_date)),
        column("created_user_id"),
        column("created_user", created_user),
        column("modified_date", lambda x: format_date(x.modified_date)),
        column("modified_user_id"),
        column("modified_user", modified_user),
    ]


class Exporter(object):
    def __init__(self, config):
        self.config = config
        self._query = []
        self._columns = []

    def get_rows(self):

        headers = [col[0] for col in self._columns]
        yield headers
        for result in self._query:
            yield [col[1](result) for col in self._columns]


@register("patients")
class PatientExporter(Exporter):
    def setup(self):
        demographics_column = demographics_column_factory(self.config)

        def d(name, getter=None, anonymised_getter=None):
            return demographics_column(name, getter, anonymised_getter, identity_getter)

        group = self.config["patient_group"]

        def recruited_user(x):
            if self.config["anonymised"]:
                return ""
            return format_user(x.recruited_user(group))

        self._columns = [
            column("patient_id", "id"),
            d("patient_number", "primary_patient_number.number"),
            d("first_name"),
            d("last_name"),
            d("date_of_birth", lambda x: format_date(x.date_of_birth)),
            column("year_of_birth"),
            d("date_of_death", lambda x: format_date(x.date_of_death)),
            column("year_of_death"),
            column("available_gender"),
            column("available_gender_label"),
            column("available_ethnicity"),
            column("patient_view", "ukrdc"),
            column("control"),
            column("signed_off_state"),
            column(
                "recruited_date", lambda x: format_date(x.recruited_date(group))
            ),  # 13
            column(
                "recruited_group_id",
                lambda x: get_attrs(x.recruited_group(group), "id"),
            ),
            column(
                "recruited_group", lambda x: get_attrs(x.recruited_group(group), "name")
            ),
            column(
                "recruited_user_id", lambda x: get_attrs(x.recruited_user(group), "id")
            ),
            column("recruited_user", recruited_user),
        ]

        q = queries.get_patients(self.config)
        self._query = q


@register("patient_numbers")
class PatientNumberExporter(Exporter):
    def setup(self):
        d = demographics_column_factory(self.config)

        self._columns = [
            column("id"),
            column("patient_id"),
            column("source_group_id"),
            column("source_group", "source_group.name"),
            column("source_type"),
            column("number_group_id"),
            column("number_group", "number_group.name"),
            d("number"),
        ]
        self._columns.extend(get_meta_columns(self.config))

        q = queries.get_patient_numbers(self.config)
        self._query = q


@register("patient_addresses")
class PatientAddressExporter(Exporter):
    def setup(self):
        d = demographics_column_factory(self.config)

        self._columns = [
            column("id"),
            column("patient_id"),
            column("source_group_id"),
            column("source_group", "source_group.name"),
            column("source_type"),
            column("from_date", lambda x: format_date(x.from_date)),
            column("to_date", lambda x: format_date(x.to_date)),
            d("address1"),
            d("address2"),
            d("address3"),
            d("address4"),
            d("postcode", anonymised_getter="anonymised_postcode"),
        ]
        self._columns.extend(get_meta_columns(self.config))

        q = queries.get_patient_addresses(self.config)
        self._query = q


@register("patient_aliases")
class PatientAliasExporter(Exporter):
    def setup(self):
        d = demographics_column_factory(self.config)

        self._columns = [
            column("id"),
            column("patient_id"),
            column("source_group_id"),
            column("source_group", "source_group.name"),
            column("source_type"),
            d("first_name"),
            d("last_name"),
        ]
        self._columns.extend(get_meta_columns(self.config))

        q = queries.get_patient_aliases(self.config)
        self._query = q


@register("patient_demographics")
class PatientDemographicsExporter(Exporter):
    def setup(self):
        d = demographics_column_factory(self.config)

        self._columns = [
            column("id"),
            column("patient_id"),
            column("source_group_id"),
            column("source_group", "source_group.name"),
            column("source_type"),
            d("first_name"),
            d("last_name"),
            d("date_of_birth", lambda x: format_date(x.date_of_birth)),
            column("year_of_birth"),
            d("date_of_death", lambda x: format_date(x.date_of_death)),
            column("year_of_death"),
            column("gender"),
            column("gender_label"),
            column("ethnicity"),
            column("ethnicity_label"),
            d("home_number"),
            d("work_number"),
            d("mobile_number"),
            d("email_address"),
        ]

        self._columns.extend(get_meta_columns(self.config))

        q = queries.get_patient_demographics(self.config)
        self._query = q


@register("medications")
class MedicationExporter(Exporter):
    def setup(self):
        self._columns = [
            column("id"),
            column("patient_id"),
            column("source_group_id"),
            column("source_group", "source_group.name"),
            column("source_type"),
            column("from_date", lambda x: format_date(x.from_date)),
            column("to_date", lambda x: format_date(x.to_date)),
            column("drug_id"),
            column("drug", "drug.name"),
            column("drug_text"),
            column("dose_quantity"),
            column("dose_unit"),
            column("dose_unit_label"),
            column("dose_text"),
            column("frequency"),
            column("route"),
            column("route_label"),
        ]
        self._columns.extend(get_meta_columns(self.config))

        q = queries.get_medications(self.config)
        self._query = q


@register("current-medications")
class CurrentMedicationExporter(Exporter):
    def setup(self):
        self._columns = [
            column("id"),
            column("patient_id"),
            column("date_of_visit", lambda x: format_date(x.date_recorded)),
            column("source_group_id"),
            column("source_group", "source_group.name"),
            column("source_type"),
            column("drug_id"),
            column("drug", "drug.name"),
            column("drug_text"),
            column("dose_quantity"),
            column("dose_unit"),
            column("dose_unit_label"),
            column("dose_text"),
            column("frequency"),
            column("route"),
            column("route_label"),
        ]
        self._columns.extend(get_meta_columns(self.config))

        q = queries.get_current_medications(self.config)
        self._query = q


class DiagnosisExporter(Exporter):
    def setup(self):
        d = demographics_column_factory(self.config)

        self._columns = [
            column("id"),
            column("patient_id"),
            column("source_group_id"),
            column("source_group", "source_group.name"),
            column("source_type"),
            column("era-edta prd"),  #5
            column("icd-10"),  #6
            column("snomed ct"), #7
            column("diagnosis", "diagnosis.name"),
            column("diagnosis_text"),
            column("symptoms_date", lambda x: format_date(x.symptoms_date)),
            column("symptoms_age_years", lambda x: get_years(x.symptoms_age)),
            column("symptoms_age_months", lambda x: get_months(x.symptoms_age)),
            column("from_date", lambda x: format_date(x.from_date)),
            column("from_age_years", lambda x: get_years(x.from_age)),
            column("from_age_months", lambda x: get_months(x.from_age)),
            column("to_date", lambda x: format_date(x.to_date)),
            column("to_age_years", lambda x: get_years(x.to_age)),
            column("to_age_months", lambda x: get_months(x.to_age)),
            column("prenatal"),
            column("gene_test"),
            column("biochemistry"),
            column("clinical_picture"),
            column("biopsy"),
            column("biopsy_diagnosis"),
            column("biopsy_diagnosis_label"),
            d("comments", anonymised_getter=None)
            ]

        if self.config['patient_group'].code == 'NURTUREINS':            
            self._columns.extend(
                [
                    column("INS diagnosis"), #27
                    column('INS diagnosis date'),
                    column('INS biopsy diagnosis'),
                    column('INS biopsy diagnosis label'),
                    column('INS biopsy diagnosis comments') #31                                  
                ]
            )
        self._columns.extend(get_meta_columns(self.config))
        self._query = queries.get_patient_diagnoses(self.config)
        self._primary = queries.get_primary_diagnoses(self.config)        

@register("primary-diagnoses")
class PrimaryDiagnosisExporter(DiagnosisExporter):
        
    def get_rows(self):
        headers = [col[0] for col in self._columns]
        yield headers

        # Differnet format for Nurture INS patients
        if self.config['patient_group'].code == 'NURTUREINS':

            patient_id = 0            
            row = []

            # Dictonary containing INS data to be added to Nurture INS data
            self.ins_data = {
                'pat_id': '',
                'ins_dia_name': '',
                'ins_dia_date': '',
                'ins_biopsy_dia': '',
                'ins_biopsy_dia_label': '',
                'ins_biopsy_dia_comments': ''                
            }

            for result in self._query:

                diagnosis = result.diagnosis
                if not diagnosis:                
                    continue
                # Check for new patient
                if result.patient_id != patient_id:
                    patient_id = result.patient_id
                    # Primary diagnosis found for previous patient, write row and add INS data
                    if row:                        
                        row[27] = self.ins_data['ins_dia_name']
                        self.ins_data['ins_dia_name'] = ''
                        row[28] = self.ins_data['ins_dia_date']
                        self.ins_data['ins_dia_date'] = ''
                        row[29] = self.ins_data['ins_biopsy_dia']
                        self.ins_data['ins_biopsy_dia'] = ''
                        row[30] = self.ins_data['ins_biopsy_dia_label']
                        self.ins_data['ins_biopsy_dia_label'] = ''
                        row[31] = self.ins_data['ins_biopsy_dia_comments']
                        self.ins_data['ins_biopsy_dia_comments'] = ''                        
                        yield row
                        row = self.makeRow(result, diagnosis)
                        ins_data = self.getInsData(result, diagnosis)                    
                    # No primary diagnosis found for previous patient but INS data present, write INS data
                    else:
                        if self.ins_data['ins_dia_name'] != '':
                            row = [''] * len(headers)
                            row[1] = self.ins_data['pat_id']
                            self.ins_data['pat_id'] = ''
                            row[27] = self.ins_data['ins_dia_name']
                            self.ins_data['ins_dia_name'] = ''
                            row[28] = self.ins_data['ins_dia_date']
                            self.ins_data['ins_dia_date'] = ''
                            row[29] = self.ins_data['ins_biopsy_dia']
                            self.ins_data['ins_biopsy_dia'] = ''
                            row[30] = self.ins_data['ins_biopsy_dia_label']
                            self.ins_data['ins_biopsy_dia_label'] = ''
                            row[31] = self.ins_data['ins_biopsy_dia_comments']
                            self.ins_data['ins_biopsy_dia_comments'] = ''                   
                            yield row
                            row = self.makeRow(result, diagnosis)
                            ins_data = self.getInsData(result, diagnosis)
                        # New patient, no data found for previous patient
                        else:
                            row = self.makeRow(result, diagnosis)
                            ins_data = self.getInsData(result, diagnosis)
                
                # Not new patient
                else:
                    # Primary diagnosis has been found, continue to check for INS data
                    if row:
                        ins_data = self.getInsData(result, diagnosis)
                    # Search for primary diagnosis and INS data
                    else:
                        row = self.makeRow(result, diagnosis)
                        ins_data = self.getInsData(result, diagnosis)
        
        # Not Nurture-ins export
        else:            
            for result in self._query:
                diagnosis = result.diagnosis
                if not diagnosis:
                    continue
                row = self.makeRow(result, diagnosis)
                if row:
                    yield row  

    def makeRow(self, result, diagnosis):        
        
        if diagnosis not in self._primary:
            return
        else:
            row = [col[1](result) for col in self._columns]
            
            if diagnosis and diagnosis.codes:
                for code in diagnosis.codes:
                    if code.system == "ERA-EDTA PRD":
                        row[5] = code.code                        
                    if code.system == "ICD-10":
                        row[6] = code.code                        
                    if code.system == "SNOMED CT":
                        row[7] = code.code

            return row

    def getInsData(self, result, diagnosis):

        for group_diagnosis in diagnosis.group_diagnoses:
            if group_diagnosis.group.code == 'INS' and group_diagnosis.type.value == 'PRIMARY':
                if not self.ins_data['ins_dia_date'] or self.ins_data['ins_dia_date'] < result.from_date:
                    self.ins_data['pat_id'] = result.patient_id
                    self.ins_data['ins_dia_name'] = diagnosis.name 
                    self.ins_data['ins_dia_date'] = result.from_date
                    self.ins_data['ins_biopsy_dia'] = result.biopsy_diagnosis
                    self.ins_data['ins_biopsy_dia_label'] = result.biopsy_diagnosis_label
                    self.ins_data['ins_biopsy_dia_comments'] = result.comments
        return


@register("comorbidities")
class ComorbiditiesExporter(DiagnosisExporter):
    def get_rows(self):
        headers = [col[0] for col in self._columns]
        yield headers

        for result in self._query:
            if result in self._primary:
                continue

            row = [col[1](result) for col in self._columns]
            diagnosis = result.diagnosis

            if diagnosis and diagnosis.codes:
                for code in diagnosis.codes:
                    if code.system == "ERA-EDTA PRD":
                        row[5] = code.code
                    if code.system == "ICD-10":
                        row[6] = code.code
                    if code.system == "SNOMED CT":
                        row[7] = code.code

            yield row


@register("genetics")
class GeneticsExporter(Exporter):
    def setup(self):
        self._columns = [
            column("id"),
            column("patient_id"),
            column("group_id"),
            column("group", "group.name"),
            column("date_sent", lambda x: format_date(x.date_sent)),
            column("laboratory"),
            column("reference_number"),
            column("karyotype"),
            column("karyotype_label"),
            column("results"),
            column("summary"),
        ]
        self._columns.extend(get_meta_columns(self.config))

        q = queries.get_genetics(self.config)
        self._query = q


@register("pathology")
class PathologyExporter(Exporter):
    def setup(self):
        d = demographics_column_factory(self.config)
        self._columns = [
            column("id"),
            column("patient_id"),
            column("source_group_id"),
            column("source_group", "source_group.name"),
            column("date", lambda x: format_date(x.date)),
            column("kidney_type"),
            column("kidney_type_label"),
            column("kidney_side"),
            column("kidney_side_label"),
            column("reference_number"),
            column("image_url"),
            d(
                "histological_summary",
                anonymised_getter=lambda x: x.histological_summary
                if x.histological_summary is None
                else "TEXT",
            ),
            d("em_findings", anonymised_getter=None),
        ]
        self._columns.extend(get_meta_columns(self.config))

        q = queries.get_pathology(self.config)
        self._query = q


@register("family_histories")
class FamilyHistoryExporter(Exporter):
    def setup(self):
        self._columns = [
            column("id"),
            column("patient_id"),
            column("group_id"),
            column("group", "group.name"),
            column("parental_consanguinity"),
            column("family_history"),
        ]
        self._columns.extend(get_meta_columns(self.config))

        q = queries.get_family_histories(self.config)
        self._query = q


@register("family_history_relatives")
class FamilyHistoryRelativeExporter(Exporter):
    def setup(self):
        self._columns = [
            column("id"),
            column("family_history_id"),
            column("relationship"),
            column("relationship_label"),
            column("patient_id"),
        ]

        q = queries.get_family_history_relatives(self.config)
        self._query = q


@register("ins_clinical_pictures")
class InsClinicalPictureExporter(Exporter):
    def setup(self):
        d = demographics_column_factory(self.config)
        self._columns = [
            column("id"),
            column("patient_id"),
            column("date_of_picture", lambda x: format_date(x.date_of_picture)),
            column("oedema"),
            column("hypovalaemia"),
            column("fever"),
            column("thrombosis"),
            column("peritonitis"),
            column("pulmonary_odemea"),
            column("hypertension"),
            column("rash"),
            column("rash_details"),
            column("infection"),
            column("infection_details"),
            column("ophthalmoscopy"),
            column("ophthalmoscopy_details"),
            d("comments", anonymised_getter=None),
        ]
        self._columns.extend(get_meta_columns(self.config))

        q = queries.get_ins_clinical_pictures(self.config)
        self._query = q


@register("dialysis")
class DialysisExporter(Exporter):
    def setup(self):
        self._columns = [
            column("id"),
            column("patient_id"),
            column("source_group_id"),
            column("source_group", "source_group.name"),
            column("source_type"),
            column("from_date", lambda x: format_date(x.from_date)),
            column("to_date", lambda x: format_date(x.to_date)),
            column("modality"),
            column("modality_label"),
        ]
        self._columns.extend(get_meta_columns(self.config))

        q = queries.get_dialyses(self.config)
        self._query = q


@register("plasmapheresis")
class PlasmapheresisExporter(Exporter):
    def setup(self):
        self._columns = [
            column("id"),
            column("patient_id"),
            column("source_group_id"),
            column("source_group", "source_group.name"),
            column("source_type"),
            column("from_date", lambda x: format_date(x.from_date)),
            column("to_date", lambda x: format_date(x.to_date)),
            column("no_of_exchanges"),
            column("no_of_exchanges_label"),
            column("response"),
            column("response_label"),
        ]
        self._columns.extend(get_meta_columns(self.config))

        q = queries.get_plasmapheresis(self.config)
        self._query = q


@register("transplants")
class TransplantExporter(Exporter):
    def setup(self):
        self._columns = [
            column("id"),
            column("patient_id"),
            column("source_group_id"),
            column("source_group", "source_group.name"),
            column("source_type"),
            column("transplant_group_id"),
            column("transplant_group", "transplant_group.name"),
            column("date", lambda x: format_date(x.date)),
            column("modality"),
            column("modality_label"),
            column("recipient_hla"),
            column("donor_hla"),
            column(
                "date_of_cmv_infection", lambda x: format_date(x.date_of_cmv_infection)
            ),
            column("date_of_recurrence", lambda x: format_date(x.date_of_recurrence)),
            column("date_of_failure", lambda x: format_date(x.date_of_failure)),
        ]
        self._columns.extend(get_meta_columns(self.config))

        q = queries.get_transplants(self.config)
        self._query = q


@register("transplant_biopsies")
class TransplantBiopsyExporter(Exporter):
    def setup(self):
        self._columns = [
            column("id"),
            column("transplant_id"),
            column("date_of_biopsy", lambda x: format_date(x.date_of_biopsy)),
            column("recurrence"),
        ]

        q = queries.get_transplant_biopsies(self.config)
        self._query = q


@register("transplant_rejections")
class TransplantRejectionExporter(Exporter):
    def setup(self):
        self._columns = [
            column("id"),
            column("transplant_id"),
            column("date_of_rejection", lambda x: format_date(x.date_of_rejection)),
            column("graft_loss_cause"),
        ]

        q = queries.get_transplant_rejections(self.config)
        self._query = q


@register("hospitalisations")
class HospitalisationExporter(Exporter):
    def setup(self):
        d = demographics_column_factory(self.config)
        self._columns = [
            column("id"),
            column("patient_id"),
            column("source_group_id"),
            column("source_group", "source_group.name"),
            column("source_type"),
            column("date_of_admission", lambda x: format_date(x.date_of_admission)),
            column("date_of_discharge", lambda x: format_date(x.date_of_discharge)),
            column("reason_for_admission"),
            d("comments", anonymised_getter=None),
        ]
        self._columns.extend(get_meta_columns(self.config))

        q = queries.get_hospitalisations(self.config)
        self._query = q


@register("ins_relapses")
class InsRelapseExporter(Exporter):
    def setup(self):
        self._columns = [
            column("id"),
            column("patient_id"),
            column("date_of_relapse"),
            column("kidney_type"),
            column("kidney_type_label"),
            column("viral_trigger"),
            column("immunisation_trigger"),
            column("other_trigger"),
            column("peak_pcr"),
            column("peak_acr"),
            column("peak_protein_dipstick"),
            column("remission_protein_dipstick"),
            column("high_dose_oral_prednisolone"),
            column("iv_methyl_prednisolone"),
            column("relapse_sample_taken"),
            column("date_of_remission", lambda x: format_date(x.date_of_remission)),
            column("remission_type"),
            column("remission_type_label"),
            column("remission_pcr"),
            column("remission_acr"),
        ]
        self._columns.extend(get_meta_columns(self.config))

        q = queries.get_ins_relapses(self.config)
        self._query = q


@register("mpgn_clinical_pictures")
class MpgnClinicalPicturesExporter(Exporter):
    def setup(self):
        d = demographics_column_factory(self.config)
        self._columns = [
            column("id"),
            column("patient_id"),
            column("date_of_picture", lambda x: format_date(x.date_of_picture)),
            column("oedema"),
            column("hypertension"),
            column("urticaria"),
            column("partial_lipodystrophy"),
            column("infection"),
            column("infection_details"),
            column("ophthalmoscopy"),
            column("ophthalmoscopy_details"),
            d("comments", anonymised_getter=None),
        ]
        self._columns.extend(get_meta_columns(self.config))

        q = queries.get_mpgn_clinical_pictures(self.config)
        self._query = q


@register("group_patients")
class GroupPatientExporter(Exporter):
    def setup(self):
        self._columns = [
            column("id"),
            column("patient_id"),
            column("group_id"),
            column("group", "group.name"),
            column("from_date", lambda x: format_date(x.from_date)),
            column("to_date", lambda x: format_date(x.to_date)),
            column("discharged_date", lambda x: format_date(x.discharged_date)),
            column("created_group_id"),
            column("created_group", "created_group.name"),
        ]
        self._columns.extend(get_meta_columns(self.config))

        q = queries.get_group_patients(self.config)
        self._query = q


@register("renal_progressions")
class RenalProgressionExporter(Exporter):
    def setup(self):
        self._columns = [
            column("id"),
            column("patient_id"),
            column("onset_date", lambda x: format_date(x.onset_date)),
            column("ckd3a_date", lambda x: format_date(x.ckd3a_date)),
            column("ckd3b_date", lambda x: format_date(x.ckd3b_date)),
            column("ckd4_date", lambda x: format_date(x.ckd4_date)),
            column("ckd5_date", lambda x: format_date(x.ckd5_date)),
            column("esrf_date", lambda x: format_date(x.esrf_date)),
        ]
        self._columns.extend(get_meta_columns(self.config))

        q = queries.get_renal_progressions(self.config)
        self._query = q


@register("results")
class ResultExporter(Exporter):
    def setup(self):
        self._columns = [
            column("id"),
            column("patient_id"),
            column("source_group_id"),
            column("source_group", "source_group.name"),
            column("source_type"),
            column("date"),
            column("observation_name", "observation.name"),
            column("value"),
            column("value_label"),
            column("sent_value"),
        ]
        self._columns.extend(get_meta_columns(self.config))

    def get_rows(self):
        headers = [col[0] for col in self._columns]
        yield headers

        q = queries.get_results(self.config)
        for result in q.yield_per(1000):
            yield [col[1](result) for col in self._columns]
            value = result.egfr_calculated
            if value:
                row = [col[1](result) for col in self._columns]
                row[6] = "RADAR Calculated eGFR"
                row[7] = row[9] = value
                yield row


@register("results-pivot")
class PivotedResultExporter(Exporter):
    def setup(self):
        self._columns = [
            column("patient_id"),
            column("source_group"),
            column("source_type"),
            column("date"),
        ]

    def get_rows(self):
        observations = queries.get_observations()
        for observation in observations:
            self._columns.append(column(observation.short_name))

        headers = [col[0] for col in self._columns]
        yield headers

        for patient in queries.get_patients(self.config):
            data = {}
            for result in patient.results:
                try:
                    date_str = result.date.strftime("%Y-%m-%dT%H:%M:%S")
                except ValueError:
                    date_str = "bad_date"
                key = (result.source_group.name, result.source_type, date_str)
                if key not in data:
                    data[key] = {}
                data[key][result.observation.short_name] = result.sent_value

            for key, items in sorted(data.items(), key=lambda x: x[0][2]):
                row = [patient.id, key[0], key[1], key[2]]
                for observation in headers[4:]:
                    row.append(items.get(observation, None))

                yield row


#     def run(self):
#         q = queries.get_results(self.config)
#         self._query = q

#     @property
#     def dataset(self):
#         egfr_calculated = 'Estimated GFR Calculated'
#         extra = {row.observation.name for row in self._query}
#         extra.add(egfr_calculated)
#         extra = sorted(extra, key=lambda val: val.lower())

#         self._columns.extend(column(name) for name in extra)

#         data = OrderedDict()

#         for row in self._query:
#             key = (row.patient_id, row.source_group.name, row.source_type, row.date)
#             if key not in data:
#                 data[key] = {egfr_calculated: ''}

#             data[key][row.observation.name] = row.value_label_or_value

#             if data[key][egfr_calculated] == '':
#                 data[key][egfr_calculated] = row.egfr_calculated

#         dataset = make_dataset(self._columns, results=True)

#         for key, results in data.items():
#             row = list(key)
#             try:
#                 row[3] = row[3].strftime('%d/%m/%Y %H:%M:%S')
#             except ValueError:
#                 year, month, day, hour, minute, second = row[3].timetuple()[:6]
#                 row[3] = '{}/{}/{} {}:{}:{}'.format(day, month, year, hour, minute, second)

#             for test in extra:
#                 if test in results:
#                     row.append(results[test])
#                 else:
#                     row.append('')
#             dataset.append(row)

#         return dataset


@register("observations")
class ObservationExporter(Exporter):
    def setup(self):
        self._columns = [
            column("id"),
            column("name"),
            column("short_name"),
            column("value_type"),
            column("sample_type"),
            column("pv_code"),
            column("min_value"),
            column("max_value"),
            column("min_length"),
            column("max_length"),
            column("units"),
            column("options"),
        ]

        self._query = Observation.query.order_by(Observation.id)


@register("6cit")
class Cit6Exporter(Exporter):
    def setup(self):
        self._columns = [
            column("id"),
            column("patient_id"),
            column("date", "data.date"),
            column("q1", "data.q1"),
            column("q2", "data.q2"),
            column("q4", "data.q4"),
            column("q5", "data.q5"),
            column("q6", "data.q6"),
            column("q7", "data.q7"),
            column("score", "data.score"),
        ]
        self._columns.extend(get_meta_columns(self.config))
        q = queries.get_form_data(self.config)
        self._query = q


@register("chu9d")
class CHU9DExporter(Exporter):
    def setup(self):
        self._columns = [
            column("id"),
            column("patient_id"),
            column("date", "data.date"),
            column("worried", "data.worried"),
            column("sad", "data.sad"),
            column("pain", "data.pain"),
            column("tired", "data.tired"),
            column("annoyed", "data.annoyed"),
            column("work", "data.work"),
            column("sleep", "data.sleep"),
            column("routine", "data.routine"),
            column("activities", "data.activities"),
        ]
        self._columns.extend(get_meta_columns(self.config))
        q = queries.get_form_data(self.config)
        self._query = q


@register("diabetic-complications")
class DiabeticComplicationExporter(Exporter):
    def setup(self):
        self._columns = [
            column("id"),
            column("patient_id"),
            column("laser", "data.laser"),
            column("foot ulcers", "data.footUlcers"),
            column("retinopathy", "data.retinopathy"),
            column("peripheral neuropathy", "data.peripheralNeuropathy"),
        ]
        self._columns.extend(get_meta_columns(self.config))
        q = queries.get_form_data(self.config)
        self._query = q


@register("eq-5d-5l")
class Eq5d5lExporter(Exporter):
    def setup(self):
        self._columns = [
            column("id"),
            column("patient_id"),
            column("date", "data.date"),
            column("age", "data.age"),
            column("gender", "data.gender"),
            column("mobility", "data.mobility"),
            column("self care", "data.selfCare"),
            column("pain discomfort", "data.painDiscomfort"),
            column("usual activities", "data.usualActivities"),
            column("anxiety depression", "data.anxietyDepression"),
            column("health", "data.health"),
        ]
        self._columns.extend(get_meta_columns(self.config))
        q = queries.get_form_data(self.config)
        self._query = q


@register("eq-5d-y")
class Eq5dyExporter(Exporter):
    def setup(self):
        self._columns = [
            column("id"),
            column("patient_id"),
            column("date", "data.date"),
            column("age", "data.age"),
            column("gender", "data.gender"),
            column("mobility", "data.mobility"),
            column("self care", "data.selfCare"),
            column("pain discomfort", "data.painDiscomfort"),
            column("usual activities", "data.usualActivities"),
            column("anxiety depression", "data.anxietyDepression"),
            column("health", "data.health"),
        ]
        self._columns.extend(get_meta_columns(self.config))
        q = queries.get_form_data(self.config)
        self._query = q


@register("hads")
class HadsExporter(Exporter):
    def setup(self):
        self._columns = [
            column("id"),
            column("patient_id"),
            column("date", "data.date"),
            column("a1", "data.a1"),
            column("a2", "data.a2"),
            column("a3", "data.a3"),
            column("a4", "data.a4"),
            column("a5", "data.a5"),
            column("a6", "data.a6"),
            column("a7", "data.a7"),
            column("d1", "data.d1"),
            column("d2", "data.d2"),
            column("d3", "data.d3"),
            column("d4", "data.d4"),
            column("d5", "data.d5"),
            column("d6", "data.d6"),
            column("d7", "data.d7"),
            column("anxiety score", "data.anxietyScore"),
            column("depression score", "data.depressionScore"),
        ]
        self._columns.extend(get_meta_columns(self.config))
        q = queries.get_form_data(self.config)
        self._query = q


@register("family-history")
class FamilyDiseasesHistoryExporter(Exporter):
    def setup(self):
        self._columns = [
            column("id"),
            column("patient_id"),
            column("chd", "data.chd"),
            column("eskd", "data.eskd"),
            column("diabetes", "data.diabetes"),
            column("chdRelative1", "data.chdRelative1"),
            column("chdRelative2", "data.chdRelative2"),
            column("chdRelative3", "data.chdRelative3"),
            column("eskdRelative1", "data.eskdRelative1"),
            column("eskdRelative2", "data.eskdRelative2"),
            column("eskdRelative3", "data.eskdRelative3"),
            column("diabetesRelative1", "data.diabetesRelative1"),
            column("diabetesRelative2", "data.diabetesRelative2"),
            column("diabetesRelative3", "data.diabetesRelative3"),
        ]
        self._columns.extend(get_meta_columns(self.config))
        q = queries.get_form_data(self.config)
        self._query = q


@register("ipos")
class IposExporter(Exporter):
    def setup(self):
        self._columns = [
            column("id"),
            column("patient_id"),
            column("date", "data.date"),
            column("score1", "data.score1"),
            column("score2", "data.score2"),
            column("score3", "data.score3"),
            column("score4", "data.score4"),
            column("score5", "data.score5"),
            column("score6", "data.score6"),
            column("score7", "data.score7"),
            column("score8", "data.score8"),
            column("score9", "data.score9"),
            column("score10", "data.score10"),
            column("score11", "data.score11"),
            column("score12", "data.score12"),
            column("score13", "data.score13"),
            column("score14", "data.score14"),
            column("score15", "data.score15"),
            column("score16", "data.score16"),
            column("score17", "data.score17"),
            column("question1", "data.question1"),
            column("score18", "data.score18"),
            column("question2", "data.question2"),
            column("score19", "data.score19"),
            column("question3", "data.question3"),
            column("score20", "data.score20"),
            column("question4", "data.question4"),
            column("question5", "data.question5"),
            column("score", "data.score"),
        ]
        self._columns.extend(get_meta_columns(self.config))
        q = queries.get_form_data(self.config)
        self._query = q


@register("samples")
class SamplesExporter(Exporter):
    def setup(self):
        self._columns = [
            column("id"),
            column("patient_id"),
            column("date", "data.date"),
            column("barcode", "data.barcode"),
        ]
        self._columns.extend(get_meta_columns(self.config))
        q = queries.get_form_data(self.config)
        self._query = q


@register("anthropometrics")
class AnthropometricsExporter(Exporter):
    def setup(self):
        self._columns = [
            column("id"),
            column("patient_id"),
            column("date", "data.date"),
            column("height", "data.height"),
            column("weight", "data.weight"),
            column("hip", "data.hip"),
            column("waist", "data.waist"),
            column("arm", "data.arm"),
            column("up", "data.up"),
            column("gripDominant", "data.gripDominant"),
            column("gripNonDominant", "data.gripNonDominant"),
            column("karnofsky", "data.karnofsky"),
            column("systolic1", "data.systolic1"),
            column("systolic2", "data.systolic2"),
            column("systolic3", "data.systolic3"),
            column("systolic", "data.systolic"),
            column("diastolic1", "data.diastolic1"),
            column("diastolic2", "data.diastolic2"),
            column("diastolic3", "data.diastolic3"),
            column("diastolic", "data.diastolic"),
        ]
        self._columns.extend(get_meta_columns(self.config))
        q = queries.get_form_data(self.config)
        self._query = q


@register("socio-economic")
class SocioEconomicExporter(Exporter):
    def setup(self):
        self._columns = [
            column("id"),
            column("patient_id"),
            column("date", "data.date"),
            column("maritalStatus", "data.maritalStatus"),
            column("education", "data.education"),
            column("employmentStatus", "data.employmentStatus"),
            column("firstLanguage", "data.firstLanguage"),
            column("literacy", "data.literacy"),
            column("literacyHelp", "data.literacyHelp"),
            column("smoking", "data.smoking"),
            column("cigarettesPerDay", "data.cigarettesPerDay"),
            column("alcohol", "data.alcohol"),
            column("unitsPerWeek", "data.unitsPerWeek"),
            column("diet", "data.diet"),
            column("otherDiet", "data.otherDiet"),
        ]
        self._columns.extend(get_meta_columns(self.config))
        q = queries.get_form_data(self.config)
        self._query = q


@register("nurtureckd")
class NurtureCKDExporter(Exporter):
    def setup(self):
        self._columns = [
            column("id"),
            column("patient_id"),
            column("date", "data.date"),
            column("visit", "data.visit"),
            column("comorbidities", "data.comorbities"),
            column("vaccinationFlu", "data.vaccinationFlu"),
            column("vaccinationPneumonia", "data.vaccinationPneumonia"),
            column("admission", "data.admission"),
            column("admissionNumber", "data.admissionNumber"),
            column("admissionEmergency", "data.admissionEmergency"),
            column("admissionPlanned", "data.admissionPlanned"),
            column("admissionDays", "data.admissionDays"),
            column("admissionAntibiotics", "data.admissionAntibiotics"),
            column("medicine1", "data.medicine1"),
            column("tabletsParacetamol", "data.tabletsParacetamol"),
            column("yearsParacetamol", "data.yearsParacetamol"),
            column("medicine2", "data.medicine2"),
            column("tabletsCocodamol", "data.tabletsCocodamol"),
            column("yearsCocodamol", "data.yearsCocodamol"),
            column("medicine3", "data.medicine3"),
            column("tabletsIbuprofen", "data.tabletsIbuprofen"),
            column("yearsIbuprofen", "data.yearsIbuprofen"),
        ]
        self._columns.extend(get_meta_columns(self.config))
        q = queries.get_form_data(self.config)
        self._query = q


@register("renal_imaging")
class RenalImagingExporter(Exporter):
    def setup(self):
        self._columns = [
            column("id"),
            column("patient_id"),
            column("source_group_id"),
            column("source_group", "source_group.name"),
            column("source_type"),
            column("date", lambda x: format_date(x.date)),
            column("imaging_type"),
            column("right_present"),
            column("right_type"),
            column("right_length"),
            column("right_volume"),
            column("right_cysts"),
            column("right_stones"),
            column("right_calcification"),
            column("right_nephrocalcinosis"),
            column("right_nephrolithiasis"),
            column("right_other_malformation"),
            column("left_present"),
            column("left_type"),
            column("left_length"),
            column("left_volume"),
            column("left_cysts"),
            column("left_stones"),
            column("left_calcification"),
            column("left_nephrocalcinosis"),
            column("left_nephrolithiasis"),
            column("left_other_malformation"),
        ]

        self._columns.extend(get_meta_columns(self.config))

        q = queries.get_renal_imaging(self.config)
        self._query = q


@register("consultants")
class ConsultantsExporter(Exporter):
    def setup(self):
        self._columns = [
            column("id"),
            column("first_name"),
            column("last_name"),
            column("email"),
            column("telephone_number"),
            column("gmc_number"),
            column("specialty", "specialty.name"),
        ]
        q = queries.get_consultants(self.config)
        self._query = q


@register("pregnancies")
class PregnanciesExporter(Exporter):
    def setup(self):
        self._columns = [
            column("id"),
            column("patient_id"),
            column("pregnancy_number"),
            column("date_of_lmp", lambda x: format_date(x.date_of_lmp)),
            column("gravidity"),
            column("parity1"),
            column("parity2"),
            column("outcome"),
            column("weight"),
            column("weight_centile"),
            column("gestational_age"),
            column("delivery_method"),
            column("neonatal_intensive_care"),
            column("pre_eclampsia"),
        ]

        self._columns.extend(get_meta_columns(self.config))

        q = queries.get_pregnancies(self.config)
        self._query = q


@register("fetal_ultrasounds")
class FetalUltrasoundsExporter(Exporter):
    def setup(self):
        d = demographics_column_factory(self.config)
        self._columns = [
            column("id"),
            column("patient_id"),
            column("source_group_id"),
            column("source_group", "source_group.name"),
            column("source_type"),
            column("date_of_scan", lambda x: format_date(x.date_of_scan)),
            column("fetal_identifier"),
            column("gestational_age"),
            column("head_centile"),
            column("abdomen_centile"),
            column("uterine_artery_notched"),
            column("liquor_volume"),
            d("comments", anonymised_getter=None),
        ]

        self._columns.extend(get_meta_columns(self.config))

        q = queries.get_fetal_ultrasounds(self.config)
        self._query = q


@register("clinical_features")
class ClinicalFeaturesExporter(Exporter):
    def setup(self):
        d = demographics_column_factory(self.config)
        self._columns = [
            column("id"),
            column("patient_id"),
            column("normal_pregnancy"),
            d("abnormal_pregnancy_text", anonymised_getter=None),
            column("neurological_problems"),
            column("seizures"),
            column("abnormal_gait"),
            column("deafness"),
            column("other_neurological_problem"),
            d("other_neurological_problem_text", anonymised_getter=None),
            column("joint_problems"),
            column("joint_problems_age"),
            column("x_ray_abnormalities"),
            column("chondrocalcinosis"),
            column("other_x_ray_abnormality"),
            d("other_x_ray_abnormality_text", anonymised_getter=None),
        ]

        self._columns.extend(get_meta_columns(self.config))
        q = queries.get_clinical_features(self.config)
        self._query = q


@register("liver-imaging")
class LiverImagingExporter(Exporter):
    def setup(self):
        self._columns = [
            column("id"),
            column("patient_id"),
            column("source_group", "source_group.name"),
            column("source_type"),
            column("date", lambda x: format_date(x.date)),
            column("imaging_type"),
            column("size"),
            column("hepatic_fibrosis"),
            column("hepatic_cysts"),
            column("bile_duct_cysts"),
            column("dilated_bile_ducts"),
            column("cholangitis"),
        ]
        q = queries.get_liver_imaging(self.config)
        self._query = q


@register("liver-diseases")
class LiverDiseasesExporter(Exporter):
    def setup(self):
        self._columns = [
            column("id"),
            column("patient_id"),
            column("portal_hypertension"),
            column("portal_hypertension_date"),
            column("ascites"),
            column("ascites_date", lambda x: format_date(x.ascites_date)),
            column("oesophageal"),
            column("oesophageal_date", lambda x: format_date(x.oesophageal_date)),
            column("oesophageal_bleeding"),
            column(
                "oesophageal_bleeding_date",
                lambda x: format_date(x.oesophageal_bleeding_date),
            ),
            column("gastric"),
            column("gastric_date", lambda x: format_date(x.gastric_date)),
            column("gastric_bleeding"),
            column(
                "gastric_bleeding_date", lambda x: format_date(x.gastric_bleeding_date)
            ),
            column("anorectal"),
            column("anorectal_date", lambda x: format_date(x.anorectal_date)),
            column("anorectal_bleeding"),
            column(
                "anorectal_bleeding_date",
                lambda x: format_date(x.anorectal_bleeding_date),
            ),
            column("cholangitis_acute"),
            column(
                "cholangitis_acute_date",
                lambda x: format_date(x.cholangitis_acute_date),
            ),
            column("cholangitis_recurrent"),
            column(
                "cholangitis_recurrent_date",
                lambda x: format_date(x.cholangitis_recurrent_date),
            ),
            column("spleen_palpable"),
            column(
                "spleen_palpable_date", lambda x: format_date(x.spleen_palpable_date)
            ),
        ]
        q = queries.get_liver_diseases(self.config)
        self._query = q


@register("liver-transplants")
class LiverTransplantsExporter(Exporter):
    def setup(self):
        self._columns = [
            column("id"),
            column("patient_id"),
            column("source_group", "source_group.name"),
            column("source_type"),
            column("transplant_group", "transplant_group.name"),
            column("registration_date", lambda x: format_date(x.registration_date)),
            column("transplant_date", lambda x: format_date(x.transplant_date)),
            column("indications"),
            column("other_indications"),
            column("first_graft_source"),
            column("loss_reason"),
            column("other_loss_reason"),
        ]
        q = queries.get_liver_transplants(self.config)
        self._query = q


@register("nephrectomies")
class NephrectomiesExporter(Exporter):
    def setup(self):
        self._columns = [
            column("id"),
            column("patient_id"),
            column("source_group", "source_group.name"),
            column("source_type"),
            column("date", lambda x: format_date(x.date)),
            column("kidney_side"),
            column("kidney_type"),
            column("entry_type"),
        ]
        q = queries.get_nephrectomies(self.config)
        self._query = q


@register("nutrition")
class NutritionExporter(Exporter):
    def setup(self):
        self._columns = [
            column("id"),
            column("patient_id"),
            column("source_group", "source_group.name"),
            column("source_type"),
            column("feeding_type"),
            column("from_date", lambda x: format_date(x.from_date)),
            column("to_date", lambda x: format_date(x.to_date)),
        ]
        q = queries.get_nutrition(self.config)
        self._query = q


@register("consents")
class ConsentsExporter(Exporter):
    def setup(self):
        self._columns = [
            column("id"),
            column("patient_id"),
            column("consent", "consent.label"),
            column("signed_on_date", lambda x: format_date(x.signed_on_date)),
            column(
                "reconsent_letter_sent_date",
                lambda x: format_date(x.reconsent_letter_sent_date),
            ),
            column(
                "reconsent_letter_returned_date",
                lambda x: format_date(x.reconsent_letter_returned_date),
            ),
        ]
        q = queries.get_consents(self.config)
        self._query = q


@register("alport-clinical-pictures")
class AlportPicturesExporter(Exporter):
    def setup(self):
        self._columns = [
            column("id"),
            column("patient_id"),
            column("date_of_picture", lambda x: format_date(x.date_of_picture)),
            column("deafness"),
            column("deafness_date", lambda x: format_date(x.deafness_date)),
            column("hearing_aid_date", lambda x: format_date(x.hearing_aid_date)),
        ]
        self._columns.extend(get_meta_columns(self.config))
        q = queries.get_alport_clinical_pictures(self.config)
        self._query = q


@register("rituximab-criteria")
class RituximabConsentsExporter(Exporter):
    def setup(self):
        self._columns = [
            column("id"),
            column("patient_id"),
            column("date", lambda x: format_date(x.date)),
            column("ongoing_severe_disease"),
            column("hypersensitivity"),
            column("drug_associated_toxicity"),
            column("alkylating_complication"),
            column("alkylating_failure_monitoring_requirements"),
            column("cancer"),
            column("threatened_fertility"),
            column("fall_in_egfr"),
            column("cni_therapy_complication"),
            column("cni_failure_monitoring_requirements"),
            column("diabetes"),
            column("risk_factors"),
        ]
        self._columns.extend(get_meta_columns(self.config))
        q = queries.get_rituximab_consents(self.config)
        self._query = q


@register("rituximab-baseline-assessment")
class RituximabBaselineAssessmentExporter(Exporter):
    def setup(self):
        self._columns = [
            column("id"),
            column("patient_id"),
            column("source_group", "source_group.name"),
            column("date"),
            column("nephropathy"),
            column("comorbidities"),
        ]
        q = queries.get_rituximab_baseline_assessment_data(self.config)
        self._query = q

    def get_rows(self):
        self._columns.extend(
            column(item.lower()) for item in SUPPORTIVE_MEDICATIONS.keys()
        )

        previous = (
            "chlorambucil",
            "cyclophosphamide",
            "rituximab",
            "tacrolimus",
            "cyclosporine",
        )
        with_dose = ("chlorambucil", "cyclophosphamide", "rituximab")

        for item in previous:
            items = (item, "{}_start_date".format(item), "{}_end_date".format(item))
            self._columns.extend(column(item) for item in items)
            if item in with_dose:
                self._columns.append(column("{}_dose".format(item)))
        self._columns.append(column("steroids"))
        self._columns.append(column("other_previous_treatment"))
        self._columns.append(column("past_remission"))
        self._columns.append(column("performance_status"))
        self._columns.extend(get_meta_columns(self.config))
        headers = [col[0] for col in self._columns]

        yield headers

        for data in self._query:
            row = [data.id, data.patient.id, data.source_group.name, data.date]
            row.append(data.nephropathy)
            row.append(data.comorbidities)
            for supportive in SUPPORTIVE_MEDICATIONS:
                row.append(supportive in data.supportive_medication)

            for item in previous:
                treatment = None
                if data.previous_treatment:
                    treatment = data.previous_treatment.get(item, {})
                if treatment:
                    row.append(treatment.get(item))
                    row.append(treatment.get("start_date"))
                    row.append(treatment.get("end_date"))
                else:
                    row.append(False)
                    row.append("")
                    row.append("")

                if item in with_dose:
                    if treatment:
                        row.append(treatment.get("total_dose"))
                    else:
                        row.append("")

            row.append(data.steroids)
            row.append(data.other_previous_treatment)
            row.append(data.past_remission)
            row.append(data.performance_status)
            for col in self._columns[-6:]:
                row.append(col[1](data))

            yield row


@register("rituximab-administration")
class RituximabAdministrationExporter(Exporter):
    def setup(self):
        self._columns = [
            column("id"),
            column("patient_id"),
            column("date", "data.date"),
            column("drug_name", "data.drugName"),
            column("other_drug", "data.otherDrug"),
            column("dose", "data.dose"),
            column("retreatment", "data.retreatment"),
            column("toxicity", stringify_list("toxicity")),
            column("other_toxicity", "data.otherToxicity"),
        ]

        self._columns.extend(get_meta_columns(self.config))
        q = queries.get_form_data(self.config)
        self._query = q


@register("rituximab-assessment")
class RituximabFollowupAssessmentExporter(Exporter):
    def setup(self):
        self._columns = [
            column("id"),
            column("patient_id"),
            column("date", "data.date"),
            column("visit", "data.visit"),
            column("performance", "data.performance"),
            column("transplant", "data.transplant"),
            column("haemodialysis", "data.haemodialysis"),
            column("peritoneal_dialysis", "data.peritonealDialysis"),
            column("supportive_medication", stringify_list("medication")),
        ]
        self._columns.extend(get_meta_columns(self.config))
        q = queries.get_form_data(self.config)
        self._query = q


@register('rituximab-adverse-events')
class RituximabAdverseEventsExporter(Exporter):
    def setup(self):
        d = demographics_column_factory(self.config)
        self._columns = [
            column('id'),
            column('patient_id'),
            column('date', 'data.date'),
            column('hospitalisation', 'data.hospitalisation'),
            column('adverse_events', 'data.adverseEvents'),
            column('onset_cancer', 'data.newOnsetCancer'),
            column('caused_cancer', 'data.causedCancer'),
            column('thromboembolism', 'data.thromboembolism'),
            column('caused_thromboembolism', 'data.causedVenousThromboEmbolism'),
            column('myocardial_infarction', 'data.myocardialInfarction'),
            column('caused_infarction', 'data.causedAcuteMyocardialInfarction'),
            column('stroke', 'data.stroke'),
            column('caused_stroke', 'data.causedStroke'),
            column('ischaemic_attack', 'data.ischaemicAttack'),
            column('caused_attack', 'data.causedIschaemicAttack'),
            column('other_adverse_event', 'data.otherAdverseEvent'),
            column('other_toxicity', 'data.otherTox'),
            column('caused_other', 'data.causedOther'),
            column('date_of_death', 'data.dod'),
            d('cause_of_death', 'data.dodCause', anonymised_getter=None)
        ]
        self._columns.extend(get_meta_columns(self.config))
        q = queries.get_form_data(self.config)
        self._query = q


@register("adtkd-clinical-pictures")
class ADTKDClinicalPicturesExporter(Exporter):
    def setup(self):
        d = demographics_column_factory(self.config)
        self._columns = [
            column("id"),
            column("patient_id"),
            column("picture_date"),
            column("gout"),
            column("gout_date"),
            column("family_gout"),
            column("family_gout_relatives"),
            column("thp"),
            column("uti"),
            d("comments", anonymised_getter=None),
        ]
        self._columns.extend(get_meta_columns(self.config))
        q = queries.get_adtkd_clinical_pictures(self.config)
        self._query = q
