from radar.lib.data.validation import validate
from radar.lib.database import db
from radar.lib.models import ResultDefinition, \
    ResultGroupDefinition, ResultGroupResultDefinition


# TODO units
# TODO short names
# TODO names
RESULT_DEFINITIONS = [
    {
        'code': 'ACR',
        'short_name': 'ACR',
        'name': 'Albumin : Creatinine Ratio',
        'units': 'mg/mmol',
        'type': 'DECIMAL',
    },
    {
        'code': 'ADJUSTEDCALCIUM',
        'short_name': 'AdjCa',
        'name': 'Adjusted Calcium',
        'units': 'mmol/l',
        'type': 'DECIMAL',
    },
    {
        'code': 'ALBUMIN',
        'short_name': 'Alb',
        'name': 'Albumin',
        'units': 'g/l',
        'type': 'DECIMAL',
    },
    {
        'code': 'ALP',
        'short_name': 'AlkP',
        'name': 'AlkP',
    },
    {
        'code': 'ALT',
        'short_name': 'ALT',
        'name': 'ALT',
    },
    {
        'code': 'AST',
        'short_name': 'AST',
        'name': 'AST',
    },
    {
        'code': 'BILI',
        'short_name': 'Bili',
        'name': 'Bilirubin',
    },
    {
        'code': 'BPDIA',
        'short_name': 'BPdia',
        'name': 'Diastolic Blood Pressure',
        'units': 'mm Hg',
    },
    {
        'code': 'BPSYS',
        'short_name': 'BPsys',
        'name': 'Systolic Blood Pressure',
        'units': 'mm Hg',
    },
    {
        'code': 'CALCIUM',
        'short_name': 'Ca',
        'name': 'Calcium',
    },
    {
        'code': 'CHOLESTEROL',
        'short_name': 'Cholest',
        'name': 'CHOLESTEROL',
        'units': 'mmol/l',
    },
    {
        'code': 'CICLOSPORIN',
        'short_name': 'Ciclo',
        'name': 'Ciclosporin (Cyclosporine)',
    },
    {
        'code': 'CREATININE',
        'short_name': 'Creatinine',
        'name': 'Creatinine',
    },
    {
        'code': 'CRP',
        'short_name': 'CRP',
        'name': 'C-Reactive Protein',
    },
    {
        'code': 'EGFR',
        'short_name': 'eGFR',
        'name': 'Estimated GFR',
        'units': 'ml/min/1.73m2',
    },
    {
        'code': 'FERRITIN',
        'short_name': 'Ferr',
        'name': 'Ferritin',
    },
    {
        'code': 'FERRITIN',
        'short_name': 'Ferr',
        'name': 'Ferritin',
    },
    {
        'code': 'GGT',
        'short_name': 'GGT',
        'name': 'GGT',
    },
    {
        'code': 'GLUCOSE',
        'short_name': 'Gluc',
        'name': 'Glucose',
        'units': 'mmol/l'
    },
    {
        'code': 'HB',
        'short_name': 'Hb',
        'name': 'HB',
        'units': 'g/l',
    },
    {
        'code': 'HBA1C',
        'short_name': 'HbA1C',
        'name': 'HbA1C',
    },
    {
        'code': 'HC03',
        'short_name': 'Bicarb',
        'name': 'Bicarbonate',
        'units': 'mmol/l',
    },
    {
        'code': 'HEIGHT',
        'short_name': 'Height',
        'name': 'Height',
        'units': 'cm',
    },
    {
        'code': 'INR',
        'short_name': 'INR',
        'name': 'INR',
        'units': 'ratio',
    },
    {
        'code': 'IRON',
        'short_name': 'Iron',
        'name': 'Iron',
    },
    {
        'code': 'IRONSAT',
        'short_name': 'Fe Sat',
        'name': 'Iron Saturation',
    },
    {
        'code': 'KTV',
        'short_name': 'Kt/V',
        'name': 'Kt/V',
    },
    {
        'code': 'LITHIUM',
        'short_name': 'Lith',
        'name': 'Lithium',
    },
    {
        'code': 'MAGNESIUM',
        'short_name': 'Mg',
        'name': 'Magnesium',
    },
    {
        'code': 'PCR',
        'short_name': 'PCR',
        'name': 'Protein : Creatinine Ratio',
        'units': 'mg/mmol',
    },
    {
        'code': 'PHEPKU',
        'short_name': 'Phe',
        'name': 'Phenylalanine (for PKU)',
    },
    {
        'code': 'PHOSPHATE',
        'short_name': 'Phos',
        'name': 'Phosphate',
        'units': 'mmol/l',
    },
    {
        'code': 'PLATELETS',
        'short_name': 'Plats',
        'name': 'Platelets',
    },
    {
        'code': 'POTASSIUM',
        'short_name': 'Potassium',
        'name': 'Potassium',
        'units': 'mmol/l',
    },
    {
        'code': 'PSA',
        'short_name': 'PSA',
        'name': 'PSA',
    },
    {
        'code': 'PTH',
        'short_name': 'PTH',
        'name': 'Parathyroid Hormone',
    },
    {
        'code': 'SIROLIMUS',
        'short_name': 'Siro',
        'name': 'Sirolimus',
    },
    {
        'code': 'SODIUM',
        'short_name': 'Sodium',
        'name': 'Sodium',
        'units': 'mmol/l',
    },
    {
        'code': 'TACROLIMUS',
        'short_name': 'Tacro',
        'name': 'Tacrolimus',
    },
    {
        'code': 'TESTOSTERONE',
        'short_name': 'Serum Testosterone',
        'name': 'Serum Testosterone',
    },
    {
        'code': 'TG',
        'short_name': 'TG',
        'name': 'Triglycerides',
    },
    {
        'code': 'TRANSFERRIN',
        'short_name': 'Tferrin',
        'name': 'Transferrin',
    },
    {
        'code': 'URATE',
        'short_name': 'Urate',
        'name': 'Uric Acid',
        'units': 'mmol/l',
    },
    {
        'code': 'UREA',
        'short_name': 'Urea',
        'name': 'Urea',
        'units': 'mmol/l',
    },
    {
        'code': 'URR',
        'short_name': 'URR',
        'name': 'Urea Reduction Ratio',
    },
    {
        'code': 'VITD',
        'short_name': 'Vit D',
        'name': 'Vitamin D',
    },
    {
        'code': 'WBC',
        'short_name': 'WBC',
        'name': 'White Blood Cell Count',
    },
    {
        'code': 'WEIGHT',
        'short_name': 'Weight',
        'name': 'Weight',
        'units': 'kg',
    }
]


# TODO short names
RESULT_GROUP_DEFINITIONS = [
    {
        'code': 'URINE',
        'name': 'Urine',
        'result_codes': [
            'ACR',
            'PCR',
        ],
    },
    {
        'code': 'LFT',
        'name': 'Liver Function Test',
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
        'result_codes': [
            'CHOLESTEROL',
            'TG',
        ],
    },
    {
        'code': 'DRUGS',
        'name': 'Drugs',
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
        'result_codes': [
            'PRE_POST_DIALYSIS',
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
        'result_codes': [
            'GLUCOSE',
            'HBA1C',
        ],
    },
    {
        'code': 'FBC',
        'name': 'Full Blood Count',
        'result_codes': [
            'HB',
            'WBC',
            'PLATELETS',
        ],
    },
    {
        'code': 'COAG',
        'name': 'Coagulation',
        'result_codes': [
            'INR',
        ],
    },
    {
        'code': 'OBV',
        'name': 'Observations',
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
        result_definition = validate(result_definition)
        db.session.add(result_definition)


def create_result_group_definitions():
    for x in RESULT_GROUP_DEFINITIONS:
        result_group_definition = ResultGroupDefinition(
            code=x['code'],
            name=x['name'],
            short_name=x['name']
        )
        result_group_definition = validate(result_group_definition)
        db.session.add(result_group_definition)

        for i, result_code in enumerate(x['result_codes']):
            result_definition = ResultDefinition.query.filter(ResultDefinition.code == result_code).one()
            result_group_result_definition = ResultGroupResultDefinition(
                result_group_definition=result_group_definition,
                result_definition=result_definition,
                weight=i,
            )
            db.session.add(result_group_result_definition)
