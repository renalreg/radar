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
            column("signed_off"),
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
            column("era-edta prd"),  # 5
            column("icd-10"),  # 6
            column("snomed ct"),  # 7
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
            d("comments", anonymised_getter=None),
        ]
        self._columns.extend(get_meta_columns(self.config))
        self._query = queries.get_patient_diagnoses(self.config)
        self._primary = queries.get_primary_diagnoses(self.config)


@register("primary-diagnoses")
class PrimaryDiagnosisExporter(DiagnosisExporter):
    def get_rows(self):
        headers = [col[0] for col in self._columns]
        yield headers

        for result in self._query:
            diagnosis = result.diagnosis
            if diagnosis not in self._primary:
                continue

            row = [col[1](result) for col in self._columns]

            if diagnosis and diagnosis.codes:
                for code in diagnosis.codes:
                    if code.system == "ERA-EDTA PRD":
                        row[5] = code.code
                    if code.system == "ICD-10":
                        row[6] = code.code
                    if code.system == "SNOMED CT":
                        row[7] = code.code

            yield row


@register("diagnoses")
# Changed for star so that all diagnoses would end up in
# the CSV. Using the star group everything become a secondary diagnoses
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
            d("histological_summary", anonymised_getter=None),
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


@register("initial-presentation")
class InitialPresentationExporter(Exporter):
    def setup(self):
        self._columns = [
            column("id"),
            column("patient_id"),
            column("date", "data.date"),
            column("presentation", "data.presentation"),
        ]


@register("consents")
class ConsentsExporter(Exporter):
    def setup(self):
        self._columns = [
            column("id"),
            column("patient_id"),
            column("consent", "consent.label"),
            column("signed_on_date", lambda x: format_date(x.signed_on_date)),
        ]
        q = queries.get_consents(self.config)
        self._query = q


@register("bsi")
class BodySystemInvolvementExporter(Exporter):
    def setup(self):
        self._columns = [
            column("id"),
            column("patient_id"),
            column("bodyInvolvement", "data.bodyInvolvement"),
        ]


@register("fhoosd")
class BodySystemInvolvementExporter(Exporter):
    def setup(self):
        self._columns = [
            column("id"),
            column("patient_id"),
            column("disease", "data.disease"),
            column("relative", "data.relative"),
        ]
        self._columns.extend(get_meta_columns(self.config))
        q = queries.get_form_data(self.config)
        self._query = q
