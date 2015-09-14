from flask import Flask
from flask_cors import CORS

from radar.api.views.patient_addresses import PatientAddressListView, PatientAddressDetailView
from radar.api.views.patient_aliases import PatientAliasListView, PatientAliasDetailView
from radar.api.views.patient_demographics import PatientDemographicsListView, PatientDemographicsDetailView, EthnicityCodeListView
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
from radar.api.views.renal_imaging import RenalImagingListView, RenalImagingDetailView
from radar.api.views.salt_wasting_clinical_features import SaltWastingClinicalFeaturesListView, \
    SaltWastingClinicalFeaturesDetailView
from radar.api.views.organisations import OrganisationListView
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

    CORS(app)

    app.before_request(require_login)

    register_template_filters(app)

    app.add_url_rule('/login', view_func=LoginView.as_view('login'))

    # Cohorts
    app.add_url_rule('/cohorts', view_func=CohortListView.as_view('cohort_list'))
    app.add_url_rule('/cohorts/<int:id>', view_func=CohortDetailView.as_view('cohort_detail'))

    # Dialysis
    app.add_url_rule('/dialysis', view_func=DialysisListView.as_view('dialysis_list'))
    app.add_url_rule('/dialysis/<int:id>', view_func=DialysisDetailView.as_view('dialysis_detail'))
    app.add_url_rule('/dialysis-types', view_func=DialysisTypeListView.as_view('dialysis_type_list'))

    # Genetics
    app.add_url_rule('/genetics', view_func=GeneticsListView.as_view('genetics_list'))
    app.add_url_rule('/genetics/<int:id>', view_func=GeneticsDetailView.as_view('genetics_detail'))

    # Hospitalisations
    app.add_url_rule('/hospitalisations', view_func=HospitalisationListView.as_view('hospitalisation_list'))
    app.add_url_rule('/hospitalisations/<int:id>', view_func=HospitalisationDetailView.as_view('hospitalisation_detail'))

    # Data Sources
    app.add_url_rule('/data-sources', view_func=DataSourceListView.as_view('data_source_list'))
    app.add_url_rule('/data-sources/<int:id>', view_func=DataSourceDetailView.as_view('data_source_detail'))

    # Medications
    app.add_url_rule('/medications', view_func=MedicationListView.as_view('medication_list'))
    app.add_url_rule('/medications/<int:id>', view_func=MedicationDetailView.as_view('medication_detail'))
    app.add_url_rule('/medication-dose-units', view_func=MedicationDoseUnitListView.as_view('medication_dose_unit_list'))
    app.add_url_rule('/medication-frequencies', view_func=MedicationFrequencyListView.as_view('medication_frequency_list'))
    app.add_url_rule('/medication-routes', view_func=MedicationRouteListView.as_view('medication_route_list'))

    # Organisations
    app.add_url_rule('/organisations', view_func=OrganisationListView.as_view('organisation_list'))

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
