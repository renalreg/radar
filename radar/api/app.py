from flask import Flask
from flask_cors import CORS
from radar.api.views.cohort_patients import CohortPatientDetailView, CohortPatientListView

from radar.api.views.cohort_users import CohortUserListView, CohortUserDetailView, CohortUserRoleListView
from radar.api.views.comorbidities import DisorderListView, ComorbidityDetailView, ComorbidityListView
from radar.api.views.diagnoses import DiagnosisListView, DiagnosisDetailView, CohortDiagnosisListView, \
    DiagnosisBiopsyDiagnosesListView, DiagnosisKaryotypeListView
from radar.api.views.family_history import FamilyHistoryListView, FamilyHistoryDetailView
from radar.api.views.logout import LogoutView
from radar.api.views.organisation_patients import OrganisationPatientListView, OrganisationPatientDetailView
from radar.api.views.organisation_users import OrganisationUserListView, OrganisationUserDetailView, \
    OrganisationUserRoleListView
from radar.api.views.pathology import PathologyDetailView, PathologyListView, PathologyKidneyTypeListView, \
    PathologyKidneySideListView
from radar.api.views.patient_addresses import PatientAddressListView, PatientAddressDetailView
from radar.api.views.patient_aliases import PatientAliasListView, PatientAliasDetailView
from radar.api.views.patient_demographics import PatientDemographicsListView, PatientDemographicsDetailView, \
    EthnicityCodeListView, GenderListView
from radar.api.views.dialysis import DialysisListView, DialysisDetailView, DialysisTypeListView
from radar.api.views.cohorts import CohortListView, CohortDetailView
from radar.api.views.data_sources import DataSourceListView, DataSourceDetailView
from radar.api.views.genetics import GeneticsDetailView, GeneticsListView
from radar.api.views.hospitalisations import HospitalisationDetailView, HospitalisationListView
from radar.api.views.medications import MedicationDetailView, MedicationListView, MedicationDoseUnitListView, \
    MedicationRouteListView, MedicationFrequencyListView
from radar.api.views.patient_numbers import PatientNumberListView, PatientNumberDetailView
from radar.api.views.patients import PatientListView, PatientDetailView
from radar.api.views.plasmapheresis import PlasmapheresisListView, PlasmapheresisDetailView, \
    PlasmapheresisResponseListView, PlasmapheresisNoOfExchangesListView
from radar.api.views.posts import PostListView, PostDetailView
from radar.api.views.renal_imaging import RenalImagingListView, RenalImagingDetailView, RenalImagingTypeListView, \
    RenalImagingKidneyTypeListView
from radar.api.views.salt_wasting_clinical_features import SaltWastingClinicalFeaturesListView, \
    SaltWastingClinicalFeaturesDetailView
from radar.api.views.organisations import OrganisationListView, OrganisationDetailView
from radar.api.views.transplants import TransplantListView, TransplantDetailView, TransplantTypeListView
from radar.api.views.users import UserDetailView, UserListView
from radar.api.views.login import LoginView
from radar.lib.auth import require_login
from radar.lib.database import db
from radar.lib.template_filters import register_template_filters


def create_app():
    app = Flask(__name__)
    app.config.from_object('radar.default_settings')
    app.config.from_object('radar.api.default_settings')
    app.config.from_envvar('RADAR_SETTINGS')

    db.init_app(app)

    if app.debug:
        CORS(app)

    app.before_request(require_login)

    register_template_filters(app)

    app.add_url_rule('/login', view_func=LoginView.as_view('login'))
    app.add_url_rule('/logout', view_func=LogoutView.as_view('logout'))

    # Cohorts
    app.add_url_rule('/cohorts', view_func=CohortListView.as_view('cohort_list'))
    app.add_url_rule('/cohorts/<int:id>', view_func=CohortDetailView.as_view('cohort_detail'))

    # Cohort Patients
    app.add_url_rule('/cohort-patients', view_func=CohortPatientListView.as_view('cohort_patient_list'))
    app.add_url_rule('/cohort-patients/<int:id>', view_func=CohortPatientDetailView.as_view('cohort_patient_detail'))

    # Cohort Users
    app.add_url_rule('/cohort-users', view_func=CohortUserListView.as_view('cohort_user_list'))
    app.add_url_rule('/cohort-users/<int:id>', view_func=CohortUserDetailView.as_view('cohort_user_detail'))
    app.add_url_rule('/cohort-user-roles', view_func=CohortUserRoleListView.as_view('cohort_user_role_list'))

    # Comorbidities
    app.add_url_rule('/comorbidities', view_func=ComorbidityListView.as_view('comorbidity_list'))
    app.add_url_rule('/comorbidities/<int:id>', view_func=ComorbidityDetailView.as_view('comorbidity_detail'))
    app.add_url_rule('/comorbidity-disorders', view_func=DisorderListView.as_view('disorder_list'))

    # Data Sources
    app.add_url_rule('/data-sources', view_func=DataSourceListView.as_view('data_source_list'))
    app.add_url_rule('/data-sources/<int:id>', view_func=DataSourceDetailView.as_view('data_source_detail'))

    # Diagnoses
    app.add_url_rule('/diagnoses', view_func=DiagnosisListView.as_view('diagnosis_list'))
    app.add_url_rule('/diagnoses/<int:id>', view_func=DiagnosisDetailView.as_view('diagnosis_detail'))
    app.add_url_rule('/diagnosis-cohort-diagnoses', view_func=CohortDiagnosisListView.as_view('diagnosis_cohort_diagnosis_list'))
    app.add_url_rule('/diagnosis-biopsy-diagnoses', view_func=DiagnosisBiopsyDiagnosesListView.as_view('diagnosis_biopsy_diagnosis_list'))
    app.add_url_rule('/diagnosis-karyotypes', view_func=DiagnosisKaryotypeListView.as_view('diagnosis_karyotype_list'))

    # Dialysis
    app.add_url_rule('/dialysis', view_func=DialysisListView.as_view('dialysis_list'))
    app.add_url_rule('/dialysis/<int:id>', view_func=DialysisDetailView.as_view('dialysis_detail'))
    app.add_url_rule('/dialysis-types', view_func=DialysisTypeListView.as_view('dialysis_type_list'))

    # Family History
    app.add_url_rule('/family-history', view_func=FamilyHistoryListView.as_view('family_history_list'))
    app.add_url_rule('/family-history/<int:id>', view_func=FamilyHistoryDetailView.as_view('family_history_detail'))

    # Genetics
    app.add_url_rule('/genetics', view_func=GeneticsListView.as_view('genetics_list'))
    app.add_url_rule('/genetics/<int:id>', view_func=GeneticsDetailView.as_view('genetics_detail'))

    # Hospitalisations
    app.add_url_rule('/hospitalisations', view_func=HospitalisationListView.as_view('hospitalisation_list'))
    app.add_url_rule('/hospitalisations/<int:id>', view_func=HospitalisationDetailView.as_view('hospitalisation_detail'))

    # Medications
    app.add_url_rule('/medications', view_func=MedicationListView.as_view('medication_list'))
    app.add_url_rule('/medications/<int:id>', view_func=MedicationDetailView.as_view('medication_detail'))
    app.add_url_rule('/medication-dose-units', view_func=MedicationDoseUnitListView.as_view('medication_dose_unit_list'))
    app.add_url_rule('/medication-frequencies', view_func=MedicationFrequencyListView.as_view('medication_frequency_list'))
    app.add_url_rule('/medication-routes', view_func=MedicationRouteListView.as_view('medication_route_list'))

    # Organisations
    app.add_url_rule('/organisations', view_func=OrganisationListView.as_view('organisation_list'))
    app.add_url_rule('/organisations/<int:id>', view_func=OrganisationDetailView.as_view('organisation_detail'))

    # Organisation Patients
    app.add_url_rule('/organisation-patients', view_func=OrganisationPatientListView.as_view('organisation_patient_list'))
    app.add_url_rule('/organisation-patients/<int:id>', view_func=OrganisationPatientDetailView.as_view('organisation_patient_detail'))

    # Organisation Users
    app.add_url_rule('/organisation-users', view_func=OrganisationUserListView.as_view('organisation_user_list'))
    app.add_url_rule('/organisation-users/<int:id>', view_func=OrganisationUserDetailView.as_view('organisation_user_detail'))
    app.add_url_rule('/organisation-user-roles', view_func=OrganisationUserRoleListView.as_view('organisation_user_role_list'))

    # Pathology
    app.add_url_rule('/pathology', view_func=PathologyListView.as_view('pathology_list'))
    app.add_url_rule('/pathology/<int:id>', view_func=PathologyDetailView.as_view('pathology_detail'))
    app.add_url_rule('/pathology-kidney-types', view_func=PathologyKidneyTypeListView.as_view('pathology_kidney_type_list'))
    app.add_url_rule('/pathology-kidney-sides', view_func=PathologyKidneySideListView.as_view('pathology_kidney_side_list'))

    # Patient Addresses
    app.add_url_rule('/patient-addresses', view_func=PatientAddressListView.as_view('patient_address_list'))
    app.add_url_rule('/patient-addresses/<int:id>', view_func=PatientAddressDetailView.as_view('patient_address_detail'))

    # Patient Aliases
    app.add_url_rule('/patient-aliases', view_func=PatientAliasListView.as_view('patient_alias_list'))
    app.add_url_rule('/patient-aliases/<int:id>', view_func=PatientAliasDetailView.as_view('patient_alias_detail'))

    # Patient Demographics
    app.add_url_rule('/patient-demographics', view_func=PatientDemographicsListView.as_view('patient_demographics_list'))
    app.add_url_rule('/patient-demographics/<int:id>', view_func=PatientDemographicsDetailView.as_view('patient_demographics_detail'))
    app.add_url_rule('/ethnicity-codes', view_func=EthnicityCodeListView.as_view('ethnicity_code_list'))
    app.add_url_rule('/genders', view_func=GenderListView.as_view('gender_list'))

    # Patient Numbers
    app.add_url_rule('/patient-numbers', view_func=PatientNumberListView.as_view('patient_number_list'))
    app.add_url_rule('/patient-numbers/<int:id>', view_func=PatientNumberDetailView.as_view('patient_number_detail'))

    # Patients
    app.add_url_rule('/patients', view_func=PatientListView.as_view('patient_list'))
    app.add_url_rule('/patients/<int:id>', view_func=PatientDetailView.as_view('patient_detail'))

    # Plasmapheresis
    app.add_url_rule('/plasmapheresis', view_func=PlasmapheresisListView.as_view('plasmapheresis_list'))
    app.add_url_rule('/plasmapheresis/<int:id>', view_func=PlasmapheresisDetailView.as_view('plasmapheresis_detail'))
    app.add_url_rule('/plasmapheresis-responses', view_func=PlasmapheresisResponseListView.as_view('plasmapheresis_response_list'))
    app.add_url_rule('/plasmapheresis-no-of-exchanges', view_func=PlasmapheresisNoOfExchangesListView.as_view('plasmapheresis_no_of_exchanges_list'))

    # Posts
    app.add_url_rule('/posts', view_func=PostListView.as_view('post_list'))
    app.add_url_rule('/posts/<int:id>', view_func=PostDetailView.as_view('post_detail'))

    # Renal Imaging
    app.add_url_rule('/renal-imaging', view_func=RenalImagingListView.as_view('renal_imaging_list'))
    app.add_url_rule('/renal-imaging/<int:id>', view_func=RenalImagingDetailView.as_view('renal_imaging_detail'))
    app.add_url_rule('/renal-imaging-types', view_func=RenalImagingTypeListView.as_view('renal_imaging_type_list'))
    app.add_url_rule('/renal-imaging-kidney-types', view_func=RenalImagingKidneyTypeListView.as_view('renal_imaging_kidney_type_list'))

    # Salt Wasting Clinical Features
    app.add_url_rule('/salt-wasting-clinical-features', view_func=SaltWastingClinicalFeaturesListView.as_view('salt_wasting_clinical_features_list'))
    app.add_url_rule('/salt-wasting-clinical-features/<int:id>', view_func=SaltWastingClinicalFeaturesDetailView.as_view('salt_wasting_clinical_features_detail'))

    # Transplants
    app.add_url_rule('/transplants', view_func=TransplantListView.as_view('transplant_list'))
    app.add_url_rule('/transplants/<int:id>', view_func=TransplantDetailView.as_view('transplant_detail'))
    app.add_url_rule('/transplant-types', view_func=TransplantTypeListView.as_view('transplant_type_list'))

    # Users
    app.add_url_rule('/users', view_func=UserListView.as_view('user_list'))
    app.add_url_rule('/users/<int:id>', view_func=UserDetailView.as_view('user_detail'))

    return app
