from radar.api.views import (
    alport,
    consultants,
    demographics,
    diagnoses,
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


def setup(app):
    alport.register_views(app)
    consultants.register_views(app)
    demographics.register_views(app)
    diagnoses.register_views(app)
    dialysis.register_views(app)
    environment.register_views(app)
    family_histories.register_views(app)
    fetal_anomaly_scans.register_views(app)
    fetal_ultrasounds.register_views(app)
    forgot_password.register_views(app)
    forgot_username.register_views(app)
    forms.register_views(app)
    fuan.register_views(app)
    genetics.register_views(app)
    groups.register_views(app)
    group_consultants.register_views(app)
    group_patients.register_views(app)
    group_users.register_views(app)
    hnf1b.register_views(app)
    hospitalisations.register_views(app)
    india_ethnicities.register_views(app)
    ins.register_views(app)
    login.register_views(app)
    logout.register_views(app)
    logs.register_views(app)
    medications.register_views(app)
    mpgn.register_views(app)
    nephrectomies.register_views(app)
    pathology.register_views(app)
    patient_addresses.register_views(app)
    patient_aliases.register_views(app)
    patient_consultants.register_views(app)
    patient_demographics.register_views(app)
    patient_numbers.register_views(app)
    patients.register_views(app)
    pkd.register_views(app)
    plasmapheresis.register_views(app)
    posts.register_views(app)
    pregnancies.register_views(app)
    random_password.register_views(app)
    recruit_patient.register_views(app)
    renal_progressions.register_views(app)
    renal_imaging.register_views(app)
    reset_password.register_views(app)
    results.register_views(app)
    roles.register_views(app)
    salt_wasting.register_views(app)
    stats.register_views(app)
    transplants.register_views(app)
    user_sessions.register_views(app)
    users.register_views(app)
