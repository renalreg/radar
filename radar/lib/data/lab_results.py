from radar.lib.database import db
from radar.models import LabGroupDefinition, LabResultDefinition, LabGroupResultDefinition


# TODO units
# TODO short names
# TODO names
LAB_RESULT_DEFINITIONS = [
    ('ACR', 'ACR', 'Albumin : Creatinine Ratio', 'mg/mmol'),
    ('ADJUSTEDCALCIUM', 'AdjCa', 'Adjusted Calcium', 'mmol/l'),
    ('ALBUMIN', 'Alb', 'Albumin', 'g/l'),
    ('ALP', 'AlkP', 'AlkP', None),
    ('ALT', 'ALT', 'ALT', None),
    ('AST', 'AST', 'AST', None),
    ('BILI', 'Bili', 'Bilirubin', None),
    ('BPDIA', 'BPdia', 'Diastolic Blood Pressure', 'mm Hg'),
    ('BPSYS', 'BPsys', 'Systolic Blood Pressure', 'mm Hg'),
    ('CALCIUM', 'Ca', 'Calcium', 'mmol/l'),
    ('CHOLESTEROL', 'Cholest', 'Cholesterol', 'mmol/l'),
    ('CICLOSPORIN', 'Ciclo', 'Ciclosporin (Cyclosporine)', None),
    ('CREATININE', 'Creatinine', 'Creatinine', 'micromol/l'),
    ('CRP', 'CRP', 'C-Reactive Protein', None),
    ('EGFR', 'eGFR', 'Estimated GFR', 'ml/min/1.73m2'),
    ('FERRITIN', 'Ferr', 'Ferritin', None),
    ('GGT', 'GGT', 'GGT', None),
    ('GLUCOSE', 'Gluc', 'Glucose', 'mmol/l'),
    ('HB', 'Hb', 'HB', 'g/l'),
    ('HBA1C', 'HbA1C', 'HbA1C', None),
    ('HCO3', 'Bicarb', 'Bicarbonate', 'mmol/l'),
    ('HEIGHT', 'Height', 'Height', 'cm'),
    ('INR', 'INR', 'INR', 'ratio'),
    ('IRON', 'Iron', 'Iron', None),
    ('IRONSAT', 'Fe Sat', 'Iron Saturation', None),
    ('KTV', 'Kt/V', 'Kt/V', None),
    ('LITHIUM', 'Lith', 'Lithium', None),
    ('MAGNESIUM', 'Mg', 'Magnesium', None),
    ('PCR', 'PCR', 'Protein : Creatinine Ratio', 'mg/mmol'),
    ('PHEPKU', 'Phe', 'Phenylalanine (for PKU)', None),
    ('PHOSPHATE', 'Phos', 'Phosphate', 'mmol/l'),
    ('PLATELETS', 'Plats', 'Platelets', None),
    ('POTASSIUM', 'Potassium', 'Potassium', 'mmol/l'),
    ('PSA', 'PSA', 'PSA', None),
    ('PTH', 'PTH', 'Parathyroid Hormone', None),
    ('SIROLIMUS', 'Siro', 'Sirolimus', None),
    ('SODIUM', 'Sodium', 'Sodium', 'mmol/l'),
    ('TACROLIMUS', 'Tacro', 'Tacrolimus', None),
    ('TESTOSTERONE', 'Serum Testosterone', 'Serum Testosterone', None),
    ('TG', 'TG', 'Triglycerides', None),
    ('TRANSFERRIN', 'Tferrin', 'Transferrin', None),
    ('URATE', 'Urate', 'Uric Acid', 'mmol/l'),
    ('UREA', 'Urea', 'Urea', 'mmol/l'),
    ('URR', 'URR', 'Urea Reduction Ratio', None),
    ('VITD', 'Vit D', 'Vitamin D', None),
    ('WBC', 'WBC', 'White Blood Cell Count', None),
    ('WEIGHT', 'Weight', 'Weight', 'kg'),
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
        'result_codes': [  # TODO order
            'CICLOSPORIN',
            'SIROLIMUS',
            'TACROLIMUS',
            'LITHIUM',
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
        'name': 'Haematinics',
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
    {
        'code': 'OBV',
        'name': 'Observations',
        'pre_post': True,
        'result_codes': [  # TODO order
            'WEIGHT',
            'HEIGHT',
            'BPDIA',
            'BPSYS',
        ]
    },
    {
        'code': 'BBC',
        'name': 'Bone Biochemistry',
        'pre_post': False,
        'result_codes': [  # TODO order
            'CALCIUM',
            'MAGNESIUM',
            'PHOSPHATE',
            'VITD',
        ]
    },
    {
        'code': 'HAM',
        'name': 'Hormones and Markers',
        'pre_post': False,
        'result_codes': [  # TODO order
            'PHEPKU',
            'PSA',
            'TESTOSTERONE',
        ]
    },
]


def create_lab_result_definitions():
    for code, short_name, name, units in LAB_RESULT_DEFINITIONS:
        lab_result_definition = LabResultDefinition(code=code, name=name, short_name=short_name, units=units)
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
