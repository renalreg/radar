from radar_fixtures.validation import validate_and_add
from radar.models import CohortDiagnosis, Cohort

# TODO
COHORT_DIAGNOSES = {
    'ALPORT': [
        'Alport Syndrome - No Histology',
        'Alport Syndrome - Histologically Proven',
        'Thin Basement Membrane Disease',
    ],
    'APRT': [
        'Adenine Phosphoribosyltransferase (APRT) Deficiency',
    ],
    'ARPKD': [
        'Autosomal Recessive Polycystic Kidney Disease',
    ],
    'AHUS': [
        'Atypical Haemolytic Uraemic Syndrome',
    ],
    'CALCIP': [],
    'CYSTIN': [
        'Cystinosis',
    ],
    'CYSURIA': [
        'Cystinuria',
    ],
    'DENTLOWE': [
        'Lowe syndome (Oculocerebrorenal Syndrome)',
        'Dent Disease',
        'Other Primary Renal Fanconi Syndrome',
    ],
    'FUAN': [
        'Uromodulin-Associated Nephropathy (Familial Juvenile Hyperuricaemic Nephropathy)',
    ],
    'HNF1B': [
        'Renal Cysts & Diabetes Syndrome',
        'Glomerulocystic Disease',
        'Multicystic Dysplastic Kidneys',
        'Inherited/Genetic Diabetes Mellitus Type II (MODY)',
    ],
    'HYPOXAL': [
        'Primary Hyperoxaluria',
        'Primary Hyperoxaluria Type I',
        'Primary Hyperoxaluria Type II',
    ],
    'HYPALK': [
        'Gitelman Syndrome',
        'Type 1 Bartter Syndrome',
        'Type 2 Bartter Syndrome',
        'Type 3 Bartter Syndrome',
        'Type 4a Bartter Syndrome',
        'Type 4b Bartter Syndrome',
        'EAST Syndrome',
        'Liddle Syndrome',
    ],
    'INS': [
        'SRNS - Primary Steroid Resistance',
        'SRNS - Secondary Steroid Resistance',
        'SRNS - Presumed Steroid Resistance',
        'SSNS - Steroid Sensitive',
        'SSNS - Steroid Dependant',
        'SSNS - Frequently Relapsing',
        'SSNS - Partial Steroid Resistance',
    ],
    'IGANEPHRO': [],
    'MPGN': [
        'MPGN (Membranoproliferative Glomerulonephritis Type II - Dense Deposit Disease)',
    ],
    'MEMNEPHRO': [],
    'NEPHROS': [],
    'NSMPGNC3': [],
    'OBS': [
        'Pregnancy',
    ],
    'PRCA': [],
    'STECHUS': [
        'STEC Associated HUS (Diarrhoea Associated)',
    ],
    'VAS': [
        'Systemic Vasculitis - ANCA Positive - No Histology',
        'Systemic Vasculitis - ANCA Negative - Histologially Proven',
    ],
}


def create_cohort_diagnoses():
    for cohort_code, cohort_diagnosis_labels in COHORT_DIAGNOSES.items():
        cohort = Cohort.query.filter(Cohort.code == cohort_code).one()

        for cohort_diagnosis_label in cohort_diagnosis_labels:
            cohort_diagnosis = CohortDiagnosis()
            cohort_diagnosis.cohort = cohort
            cohort_diagnosis.label = cohort_diagnosis_label
            validate_and_add(cohort_diagnosis)
