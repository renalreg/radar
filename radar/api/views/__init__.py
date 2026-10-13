from radar.api.views import (
    alport,
    consents,
    consultants,
    demographics,
    diagnoses,
    rituximab,
)
from radar.api.views import dialysis
from radar.api.views import environment
from radar.api.views import family_histories
from radar.api.views import fetal_anomaly_scans
from radar.api.views import fetal_ultrasounds
from radar.api.views import forgot_password
from radar.api.views import forgot_username
from radar.api.views import forms
from radar.api.views import fuan
from radar.api.views import genetics
from radar.api.views import group_consultants
from radar.api.views import group_patients
from radar.api.views import group_users
from radar.api.views import groups
from radar.api.views import hnf1b
from radar.api.views import hospitalisations
from radar.api.views import india_ethnicities
from radar.api.views import ins
from radar.api.views import login
from radar.api.views import logout
from radar.api.views import logs
from radar.api.views import medications
from radar.api.views import mpgn
from radar.api.views import nephrectomies
from radar.api.views import nurture_data
from radar.api.views import nurture_tubes
from radar.api.views import pathology
from radar.api.views import patient_addresses
from radar.api.views import patient_aliases
from radar.api.views import patient_consultants
from radar.api.views import patient_demographics
from radar.api.views import patient_numbers
from radar.api.views import patients
from radar.api.views import pkd
from radar.api.views import plasmapheresis
from radar.api.views import posts
from radar.api.views import pregnancies
from radar.api.views import random_password
from radar.api.views import recruit_patient
from radar.api.views import renal_imaging
from radar.api.views import renal_progressions
from radar.api.views import reset_password
from radar.api.views import results
from radar.api.views import roles
from radar.api.views import salt_wasting
from radar.api.views import stats
from radar.api.views import transplants
from radar.api.views import user_sessions
from radar.api.views import users
from radar.variants import pick


# Registered in every deployment
COMMON_VIEW_MODULES = [
    alport,
    consents,
    consultants,
    demographics,
    diagnoses,
    dialysis,
    environment,
    family_histories,
    fetal_anomaly_scans,
    fetal_ultrasounds,
    forgot_password,
    forgot_username,
    forms,
    fuan,
    genetics,
    groups,
    group_consultants,
    group_patients,
    group_users,
    hnf1b,
    hospitalisations,
    india_ethnicities,
    ins,
    login,
    logout,
    logs,
    medications,
    mpgn,
    nephrectomies,
    nurture_tubes,
    pathology,
    patient_addresses,
    patient_aliases,
    patient_consultants,
    patient_demographics,
    patient_numbers,
    patients,
    pkd,
    plasmapheresis,
    posts,
    pregnancies,
    random_password,
    recruit_patient,
    renal_progressions,
    renal_imaging,
    reset_password,
    results,
    rituximab,
    roles,
    salt_wasting,
    stats,
    transplants,
    user_sessions,
    users,
]

MAIN_VIEW_MODULES = [
    nurture_data,
]

INTERNATIONAL_VIEW_MODULES:list(any) = []

VIEW_MODULES = COMMON_VIEW_MODULES + pick(
    main=MAIN_VIEW_MODULES,
    international=INTERNATIONAL_VIEW_MODULES,
)


def setup(app):
    for module in VIEW_MODULES:
        module.register_views(app)
