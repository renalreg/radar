from radar.models.users import User
from radar.models.posts import Post
from radar.models.patient_demographics import PatientDemographics
from radar.models.dialysis import Dialysis
from radar.models.medications import Medication
from radar.models.patients import Patient
from radar.models.transplants import Transplant
from radar.models.hospitalisations import Hospitalisation
from radar.models.plasmapheresis import Plasmapheresis
from radar.models.renal_imaging import RenalImaging
from radar.models.patient_aliases import PatientAlias
from radar.models.patient_numbers import PatientNumber
from radar.models.patient_addresses import PatientAddress
from radar.models.comorbidities import Disorder
from radar.models.diagnoses import GroupDiagnosis
from radar.models.groups import Group, GroupPatient, GroupUser
from radar.models.results import Result
from radar.models.consultants import Consultant
from radar.models.source_types import SourceType
from radar.validation.comorbidities import DisorderValidation
from radar.validation.dialysis import DialysisValidation
from radar.validation.hospitalisations import HospitalisationValidation
from radar.validation.medications import MedicationValidation
from radar.validation.patient_addresses import PatientAddressValidation
from radar.validation.patient_aliases import PatientAliasValidation
from radar.validation.patient_demographics import PatientDemographicsValidation
from radar.validation.patient_numbers import PatientNumberValidation
from radar.validation.patients import PatientValidation
from radar.validation.plasmapheresis import PlasmapheresisValidation
from radar.validation.posts import PostValidation
from radar.validation.renal_imaging import RenalImagingValidation
from radar.validation.results import ResultValidation
from radar.validation.transplants import TransplantValidation
from radar.validation.users import UserValidation
from radar.validation.consultants import ConsultantValidation
from radar.validation.groups import GroupValidation
from radar.validation.group_users import GroupUserValidation
from radar.validation.group_patients import GroupPatientValidation
from radar.validation.group_diagnoses import GroupDiagnosisValidation
from radar.validation.source_types import SourceTypeValidation
from radar.database import db
from radar.auth.sessions import current_user

VALIDATIONS = {
    User: UserValidation,
    Post: PostValidation,
    RenalImaging: RenalImagingValidation,
    Plasmapheresis: PlasmapheresisValidation,
    Hospitalisation: HospitalisationValidation,
    Transplant: TransplantValidation,
    Patient: PatientValidation,
    Medication: MedicationValidation,
    Dialysis: DialysisValidation,
    PatientDemographics: PatientDemographicsValidation,
    PatientAlias: PatientAliasValidation,
    PatientNumber: PatientNumberValidation,
    PatientAddress: PatientAddressValidation,
    Disorder: DisorderValidation,
    GroupDiagnosis: GroupDiagnosisValidation,
    Result: ResultValidation,
    Consultant: ConsultantValidation,
    Group: GroupValidation,
    GroupUser: GroupUserValidation,
    GroupPatient: GroupPatientValidation,
    SourceType: SourceTypeValidation,
}


def validate(obj, old_obj=None, ctx=None):
    model_class = obj.__class__
    validation_class = VALIDATIONS[model_class]
    validation = validation_class()

    if old_obj is None:
        old_obj = model_class()

    if ctx is None:
        ctx = {}

    if ctx.get('user') is None:
        ctx['user'] = current_user

    with db.session.no_autoflush:
        validation.before_update(ctx, old_obj)
        old_obj = validation.clone(old_obj)
        obj = validation.after_update(ctx, old_obj, obj)

    return obj
