from radar.lib.data.validation import validate
from radar.lib.database import db
from radar.lib.models import ResultSpec, ResultGroupSpec, ResultGroupResultSpec

# TODO ranges
RESULT_SPECS = [
    {
        'code': 'ACR',
        'short_name': 'ACR',
        'name': 'Albumin : Creatinine Ratio',
        'units': 'mg/mmol',
        'type': 'DECIMAL',
        'min_value': 0
    },
    {
        'code': 'ADJUSTEDCALCIUM',
        'short_name': 'AdjCa',
        'name': 'Adjusted Calcium',
        'units': 'mmol/l',
        'type': 'DECIMAL',
        'min_value': 0
    },
    {
        'code': 'ALBUMIN',
        'short_name': 'Alb',
        'name': 'Albumin',
        'units': 'g/l',
        'type': 'DECIMAL',
        'min_value': 0
    },
    {
        'code': 'ALP',
        'short_name': 'AlkP',
        'name': 'AlkP',
        'type': 'DECIMAL',
        'min_value': 0
    },
    {
        'code': 'ALT',
        'short_name': 'ALT',
        'name': 'ALT',
        'type': 'DECIMAL',
        'min_value': 0
    },
    {
        'code': 'AST',
        'short_name': 'AST',
        'name': 'AST',
        'type': 'DECIMAL',
        'min_value': 0
    },
    {
        'code': 'BILI',
        'short_name': 'Bili',
        'name': 'Bilirubin',
        'type': 'DECIMAL',
        'min_value': 0
    },
    {
        'code': 'BPDIA',
        'short_name': 'BPdia',
        'name': 'Diastolic Blood Pressure',
        'units': 'mm Hg',
        'type': 'DECIMAL',
        'min_value': 0
    },
    {
        'code': 'BPSYS',
        'short_name': 'BPsys',
        'name': 'Systolic Blood Pressure',
        'units': 'mm Hg',
        'type': 'DECIMAL',
        'min_value': 0
    },
    {
        'code': 'CALCIUM',
        'short_name': 'Ca',
        'name': 'Calcium',
        'type': 'DECIMAL',
        'min_value': 0
    },
    {
        'code': 'CHOLESTEROL',
        'short_name': 'Cholest',
        'name': 'CHOLESTEROL',
        'units': 'mmol/l',
        'type': 'DECIMAL',
        'min_value': 0
    },
    {
        'code': 'CICLOSPORIN',
        'short_name': 'Ciclo',
        'name': 'Ciclosporin (Cyclosporine)',
        'type': 'DECIMAL',
        'min_value': 0
    },
    {
        'code': 'CREATININE',
        'short_name': 'Creatinine',
        'name': 'Creatinine',
        'type': 'DECIMAL',
        'min_value': 0
    },
    {
        'code': 'CRP',
        'short_name': 'CRP',
        'name': 'C-Reactive Protein',
        'type': 'DECIMAL',
        'min_value': 0
    },
    {
        'code': 'EGFR',
        'short_name': 'eGFR',
        'name': 'Estimated GFR',
        'units': 'ml/min/1.73m2',
        'type': 'DECIMAL',
        'min_value': 0
    },
    {
        'code': 'FERRITIN',
        'short_name': 'Ferr',
        'name': 'Ferritin',
        'type': 'DECIMAL',
        'min_value': 0
    },
    {
        'code': 'GGT',
        'short_name': 'GGT',
        'name': 'GGT',
        'type': 'DECIMAL',
        'min_value': 0
    },
    {
        'code': 'GLUCOSE',
        'short_name': 'Gluc',
        'name': 'Glucose',
        'units': 'mmol/l',
        'type': 'DECIMAL',
        'min_value': 0
    },
    {
        'code': 'HB',
        'short_name': 'Hb',
        'name': 'HB',
        'units': 'g/l',
        'type': 'DECIMAL',
        'min_value': 0
    },
    {
        'code': 'HBA1C',
        'short_name': 'HbA1C',
        'name': 'HbA1C',
        'type': 'DECIMAL',
        'min_value': 0
    },
    {
        'code': 'HCO3',
        'short_name': 'Bicarb',
        'name': 'Bicarbonate',
        'units': 'mmol/l',
        'type': 'DECIMAL',
        'min_value': 0
    },
    {
        'code': 'HEIGHT',
        'short_name': 'Height',
        'name': 'Height',
        'units': 'cm',
        'type': 'DECIMAL',
        'min_value': 0
    },
    {
        'code': 'INR',
        'short_name': 'INR',
        'name': 'INR',
        'units': 'ratio',
        'type': 'DECIMAL',
        'min_value': 0
    },
    {
        'code': 'IRON',
        'short_name': 'Iron',
        'name': 'Iron',
        'type': 'DECIMAL',
        'min_value': 0
    },
    {
        'code': 'IRONSAT',
        'short_name': 'Fe Sat',
        'name': 'Iron Saturation',
        'type': 'DECIMAL',
        'min_value': 0
    },
    {
        'code': 'KTV',
        'short_name': 'Kt/V',
        'name': 'Kt/V',
        'type': 'DECIMAL',
        'min_value': 0
    },
    {
        'code': 'LITHIUM',
        'short_name': 'Lith',
        'name': 'Lithium',
        'type': 'DECIMAL',
        'min_value': 0
    },
    {
        'code': 'MAGNESIUM',
        'short_name': 'Mg',
        'name': 'Magnesium',
        'type': 'DECIMAL',
        'min_value': 0
    },
    {
        'code': 'PCR',
        'short_name': 'PCR',
        'name': 'Protein : Creatinine Ratio',
        'units': 'mg/mmol',
        'type': 'DECIMAL',
        'min_value': 0
    },
    {
        'code': 'PHEPKU',
        'short_name': 'Phe',
        'name': 'Phenylalanine (for PKU)',
        'type': 'DECIMAL',
        'min_value': 0
    },
    {
        'code': 'PHOSPHATE',
        'short_name': 'Phos',
        'name': 'Phosphate',
        'units': 'mmol/l',
        'type': 'DECIMAL',
        'min_value': 0
    },
    {
        'code': 'PLATELETS',
        'short_name': 'Plats',
        'name': 'Platelets',
        'type': 'DECIMAL',
        'min_value': 0
    },
    {
        'code': 'POTASSIUM',
        'short_name': 'Potassium',
        'name': 'Potassium',
        'units': 'mmol/l',
        'type': 'DECIMAL',
        'min_value': 0
    },
    {
        'code': 'PRE_POST_DIALYSIS',
        'short_name': 'Pre/Post',
        'name': 'Pre/Post Dialysis',
        'type': 'DECIMAL',  # TODO
        'min_value': 0
    },
    {
        'code': 'PSA',
        'short_name': 'PSA',
        'name': 'PSA',
        'type': 'DECIMAL',
        'min_value': 0
    },
    {
        'code': 'PTH',
        'short_name': 'PTH',
        'name': 'Parathyroid Hormone',
        'type': 'DECIMAL',
        'min_value': 0
    },
    {
        'code': 'SIROLIMUS',
        'short_name': 'Siro',
        'name': 'Sirolimus',
        'type': 'DECIMAL',
        'min_value': 0
    },
    {
        'code': 'SODIUM',
        'short_name': 'Sodium',
        'name': 'Sodium',
        'units': 'mmol/l',
        'type': 'DECIMAL',
        'min_value': 0
    },
    {
        'code': 'TACROLIMUS',
        'short_name': 'Tacro',
        'name': 'Tacrolimus',
        'type': 'DECIMAL',
        'min_value': 0
    },
    {
        'code': 'TESTOSTERONE',
        'short_name': 'Serum Testosterone',
        'name': 'Serum Testosterone',
        'type': 'DECIMAL',
        'min_value': 0
    },
    {
        'code': 'TG',
        'short_name': 'TG',
        'name': 'Triglycerides',
        'type': 'DECIMAL',
        'min_value': 0
    },
    {
        'code': 'TRANSFERRIN',
        'short_name': 'Tferrin',
        'name': 'Transferrin',
        'type': 'DECIMAL',
        'min_value': 0
    },
    {
        'code': 'URATE',
        'short_name': 'Urate',
        'name': 'Uric Acid',
        'units': 'mmol/l',
        'type': 'DECIMAL',
        'min_value': 0
    },
    {
        'code': 'UREA',
        'short_name': 'Urea',
        'name': 'Urea',
        'units': 'mmol/l',
        'type': 'DECIMAL',
        'min_value': 0
    },
    {
        'code': 'URR',
        'short_name': 'URR',
        'name': 'Urea Reduction Ratio',
        'type': 'DECIMAL',
        'min_value': 0
    },
    {
        'code': 'VITD',
        'short_name': 'Vit D',
        'name': 'Vitamin D',
        'type': 'DECIMAL',
        'min_value': 0
    },
    {
        'code': 'WBC',
        'short_name': 'WBC',
        'name': 'White Blood Cell Count',
        'type': 'DECIMAL',
        'min_value': 0
    },
    {
        'code': 'WEIGHT',
        'short_name': 'Weight',
        'name': 'Weight',
        'units': 'kg',
        'type': 'DECIMAL',
        'min_value': 0
    }
]

RESULT_GROUP_SPECS = [
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


def create_result_specs():
    for x in RESULT_SPECS:
        result_spec = ResultSpec()
        result_spec.code = x['code']
        result_spec.short_name = x['short_name']
        result_spec.name = x['name']
        result_spec.type = x['type']
        result_spec.units = x.get('units')
        result_spec.min_value = x.get('min_value')
        result_spec.max_value = x.get('max_value')
        result_spec = validate(result_spec)
        db.session.add(result_spec)


def create_result_group_specs():
    for x in RESULT_GROUP_SPECS:
        result_group_spec = ResultGroupSpec()
        result_group_spec.code = x['code']
        result_group_spec.name = x['name']
        result_group_spec = validate(result_group_spec)
        db.session.add(result_group_spec)

        for i, result_code in enumerate(x['result_codes']):
            result_spec = ResultSpec.query.filter(ResultSpec.code == result_code).one()
            result_group_result_spec = ResultGroupResultSpec()
            result_group_result_spec.result_group_spec = result_group_spec
            result_group_result_spec.result_spec = result_spec
            result_group_result_spec.weight = i * 100  # leave some gaps
            result_group_result_spec = validate(result_group_result_spec)
            db.session.add(result_group_result_spec)
