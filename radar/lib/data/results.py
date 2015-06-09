from radar.lib.database import db
from radar.models import ResultDefinition, \
    ResultGroupDefinition, ResultGroupResultDefinition


# TODO units
# TODO short names
# TODO names
RESULT_DEFINITIONS = [
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
RESULT_GROUP_DEFINITIONS = [
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
            'ALBUMIN',
            'ALP',
            'ALT',
            'BILI',
            'GGT',
            'AST'
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
            'PTH',
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


def create_result_definitions():
    for code, short_name, name, units in RESULT_DEFINITIONS:
        result_definition = ResultDefinition(code=code, name=name, short_name=short_name, units=units)
        db.session.add(result_definition)


def create_result_group_definitions():
    for x in RESULT_GROUP_DEFINITIONS:
        result_group_definition = ResultGroupDefinition(
            code=x['code'],
            name=x['name'],
            short_name=x['name'],
            pre_post=x['pre_post'],
        )
        db.session.add(result_group_definition)

        for i, result_code in enumerate(x['result_codes']):
            result_definition = ResultDefinition.query.filter(ResultDefinition.code == result_code).one()
            result_group_result_definition = ResultGroupResultDefinition(
                result_group_definition=result_group_definition,
                result_definition=result_definition,
                weight=i,
            )
            db.session.add(result_group_result_definition)
