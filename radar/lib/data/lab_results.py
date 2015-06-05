from radar.lib.database import db
from radar.models import LabGroupDefinition, LabResultDefinition, LabGroupResultDefinition


# TODO units
# TODO short names
# TODO names
LAB_RESULT_DEFINITIONS = [
    ('ACR', 'ACR'),
    ('PCR', 'PCR'),
    ('ADJUSTEDCALCIUM', 'Adjusted Calcium'),
    ('PHOSPHATE', 'Phosphate'),
    ('ALBUMIN', 'Albumin'),
    ('ALP', 'ALP'),
    ('ALT', 'ALT'),
    ('BILI', 'Bilirubin'),
    ('GGT', 'GGT'),
    ('CHOLESTEROL', 'Cholesterol'),
    ('TG', 'TG'),
    ('CICLOSPORIN', 'Ciclosporin'),
    ('SIROLIMUS', 'Sirolimus'),
    ('TACROLIMUS', 'Tacrolimus'),
    ('SODIUM', 'Sodium'),
    ('POTASSIUM', 'Potassium'),
    ('HCO3', 'Bicarbonate HCO3'),
    ('UREA', 'Urea'),
    ('CREATININE', 'Creatinine'),
    ('EGFR', 'eGFR'),
    ('URATE', 'Urate'),
    ('CRP', 'CRP'),
    ('URR', 'URR'),
    ('KTV', 'Kt/V'),
    ('FERRITIN', 'Ferritin'),
    ('IRON', 'Iron'),
    ('IRONSAT', 'IronSat'),
    ('TRANSFERRIN', 'Transferrin'),
    ('GLUCOSE', 'Glucose'),
    ('HBA1C', 'HbA1C'),
    ('HB', 'HB'),
    ('WBC', 'WBC'),
    ('PLATELETS', 'Platelets'),
    ('INR', 'INR'),
    ('PTH', 'PTH'),
]


# TODO short names
LAB_GROUP_DEFINITIONS = [
    {
        'code': 'URINE',
        'name': 'Urine',
        'pre_post': False,
        'result_codes': [
            'ACR',
            'PCR',
        ],
    },
    {
        'code': 'LFT',
        'name': 'Liver Function Test',
        'pre_post': False,
        'result_codes': [
            'ADJUSTEDCALCIUM',
            'PHOSPHATE',
            'ALBUMIN',
            'ALP',
            'ALT',
            'BILI',
            'GGT',
        ],
    },
    {
        'code': 'FATS',
        'name': 'Fats',
        'pre_post': False,
        'result_codes': [
            'CHOLESTEROL',
            'TG',
        ],
    },
    {
        'code': 'DRUGS',
        'name': 'Drugs',
        'pre_post': False,
        'result_codes': [
            'CICLOSPORIN',
            'SIROLIMUS',
            'TACROLIMUS',
        ],
    },
    {
        'code': 'UE',
        'name': 'Urea & Electrolytes',
        'pre_post': True,
        'result_codes': [
            'SODIUM',
            'POTASSIUM',
            'HCO3',
            'UREA',
            'CREATININE',
            'EGFR',
            'URATE',
            'CRP',
            'URR',
            'KTV',
        ],
    },
    {
        'code': 'HEAM',
        'name': 'Heamatinics',
        'pre_post': False,
        'result_codes': [
            'FERRITIN',
            'IRON',
            'IRONSAT',
            'TRANSFERRIN',
        ],
    },
    {
        'code': 'DM',
        'name': 'Diabetes Monitoring',
        'pre_post': False,
        'result_codes': [
            'GLUCOSE',
            'HBA1C',
        ],
    },
    {
        'code': 'FBC',
        'name': 'Full Blood Count',
        'pre_post': False,
        'result_codes': [
            'HB',
            'WBC',
            'PLATELETS',
        ],
    },
    {
        'code': 'COAG',
        'name': 'Coagulation',
        'pre_post': False,
        'result_codes': [
            'INR',
        ],
    },
    {
        'code': 'PTH',
        'name': 'Parathyroid Hormone',
        'pre_post': False,
        'result_codes': [
            'PTH',
        ],
    },
]


def create_lab_result_definitions():
    for code, name in LAB_RESULT_DEFINITIONS:
        lab_result_definition = LabResultDefinition(code=code, name=name, short_name=name)
        db.session.add(lab_result_definition)


def create_lab_group_definitions():
    for x in LAB_GROUP_DEFINITIONS:
        lab_group_definition = LabGroupDefinition(
            code=x['code'],
            name=x['name'],
            short_name=x['name'],
            pre_post=x['pre_post'],
        )
        db.session.add(lab_group_definition)

        for i, result_code in enumerate(x['result_codes']):
            lab_result_definition = LabResultDefinition.query.filter(LabResultDefinition.code == result_code).one()
            lab_group_result_definition = LabGroupResultDefinition(
                lab_group_definition=lab_group_definition,
                lab_result_definition=lab_result_definition,
                weight=i,
            )
            db.session.add(lab_group_result_definition)
