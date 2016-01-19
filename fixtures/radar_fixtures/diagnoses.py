from radar_fixtures.validation import validate_and_add
from radar.models.diagnoses import GroupDiagnosis
from radar.models.groups import Group, GROUP_TYPE

# TODO
GROUP_DIAGNOSES = {
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


def create_group_diagnoses():
    for code, names in GROUP_DIAGNOSES.items():
        group = Group.query.filter(Group.code == code, Group.type == GROUP_TYPE.COHORT).one()

        for i, name in enumerate(names):
            group_diagnosis = GroupDiagnosis()
            group_diagnosis.group = group
            group_diagnosis.name = name
            group_diagnosis.display_order = i
            validate_and_add(group_diagnosis)
