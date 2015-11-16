from radar.fixtures.validation import validate_and_add
from radar.models import CohortDiagnosis, Cohort

COHORT_DIAGNOSES = {
    'INS': [
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
    for cohort_code, cohort_diagnosis_labels in COHORT_DIAGNOSES.items():
        cohort = Cohort.query.filter(Cohort.code == cohort_code).one()

        for cohort_diagnosis_label in cohort_diagnosis_labels:
            cohort_diagnosis = CohortDiagnosis()
            cohort_diagnosis.cohort = cohort
            cohort_diagnosis.label = cohort_diagnosis_label
            validate_and_add(cohort_diagnosis)
