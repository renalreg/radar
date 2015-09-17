from radar.lib.data.validation import validate
from radar.lib.database import db
from radar.lib.models import CohortDiagnosis, Cohort

COHORT_DIAGNOSES = {
    'SRNS': [
        'SRNS - Primary Steroid Resistance',
        'SRNS - Secondary Steroid Resistance',
        'SRNS - Presumed Steroid Resistance',
        'SSNS - Steroid Sensitive',
        'SSNS - Steroid Dependant',
        'SSNS - Frequently Relapsing',
        'SSNS - Partial Steroid Resistance',
    ]
}


def create_cohort_diagnoses():
    for cohort_name, cohort_diagnosis_labels in COHORT_DIAGNOSES.items():
        cohort = Cohort.query.filter(Cohort.name == cohort_name).one()

        for cohort_diagnosis_label in cohort_diagnosis_labels:
            cohort_diagnosis = CohortDiagnosis()
            cohort_diagnosis.cohort = cohort
            cohort_diagnosis.label = cohort_diagnosis_label
            cohort_diagnosis = validate(cohort_diagnosis)
            db.session.add(cohort_diagnosis)
