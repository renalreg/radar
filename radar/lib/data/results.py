from collections import OrderedDict
from radar.lib.data.validation import validate
from radar.lib.database import db
from radar.lib.models import ResultSpec, ResultGroupSpec, ResultGroupResultSpec, RESULT_SPEC_TYPE_CODED_STRING, \
    RESULT_SPEC_TYPE_FLOAT

# TODO ranges
RESULT_SPECS = [
    {
        'code': 'acr',
        'short_name': 'ACR',
        'name': 'Albumin : Creatinine Ratio',
        'units': 'mg/mmol',
        'type': RESULT_SPEC_TYPE_FLOAT,
        'min_value': 0
    },
    {
        'code': 'adjustedcalcium',
        'short_name': 'AdjCa',
        'name': 'Adjusted Calcium',
        'units': 'mmol/l',
        'type': RESULT_SPEC_TYPE_FLOAT,
        'min_value': 0
    },
    {
        'code': 'albumin',
        'short_name': 'Alb',
        'name': 'Albumin',
        'units': 'g/l',
        'type': RESULT_SPEC_TYPE_FLOAT,
        'min_value': 0
    },
    {
        'code': 'alp',
        'short_name': 'AlkP',
        'name': 'AlkP',
        'type': RESULT_SPEC_TYPE_FLOAT,
        'min_value': 0
    },
    {
        'code': 'alt',
        'short_name': 'ALT',
        'name': 'ALT',
        'type': RESULT_SPEC_TYPE_FLOAT,
        'min_value': 0
    },
    {
        'code': 'ast',
        'short_name': 'AST',
        'name': 'AST',
        'type': RESULT_SPEC_TYPE_FLOAT,
        'min_value': 0
    },
    {
        'code': 'bili',
        'short_name': 'Bili',
        'name': 'Bilirubin',
        'type': RESULT_SPEC_TYPE_FLOAT,
        'min_value': 0
    },
    {
        'code': 'bpdia',
        'short_name': 'BPdia',
        'name': 'Diastolic Blood Pressure',
        'units': 'mm Hg',
        'type': RESULT_SPEC_TYPE_FLOAT,
        'min_value': 0
    },
    {
        'code': 'bpsys',
        'short_name': 'BPsys',
        'name': 'Systolic Blood Pressure',
        'units': 'mm Hg',
        'type': RESULT_SPEC_TYPE_FLOAT,
        'min_value': 0
    },
    {
        'code': 'calcium',
        'short_name': 'Ca',
        'name': 'Calcium',
        'type': RESULT_SPEC_TYPE_FLOAT,
        'min_value': 0
    },
    {
        'code': 'cholesterol',
        'short_name': 'Cholest',
        'name': 'Cholesterol',
        'units': 'mmol/l',
        'type': RESULT_SPEC_TYPE_FLOAT,
        'min_value': 0
    },
    {
        'code': 'ciclosporin',
        'short_name': 'Ciclo',
        'name': 'Ciclosporin (Cyclosporine)',
        'type': RESULT_SPEC_TYPE_FLOAT,
        'min_value': 0
    },
    {
        'code': 'creatinine',
        'short_name': 'Creatinine',
        'name': 'Creatinine',
        'type': RESULT_SPEC_TYPE_FLOAT,
        'min_value': 0
    },
    {
        'code': 'crp',
        'short_name': 'CRP',
        'name': 'C-Reactive Protein',
        'type': RESULT_SPEC_TYPE_FLOAT,
        'min_value': 0
    },
    {
        'code': 'egfr',
        'short_name': 'eGFR',
        'name': 'Estimated GFR',
        'units': 'ml/min/1.73m2',
        'type': RESULT_SPEC_TYPE_FLOAT,
        'min_value': 0
    },
    {
        'code': 'ferritin',
        'short_name': 'Ferr',
        'name': 'Ferritin',
        'type': RESULT_SPEC_TYPE_FLOAT,
        'min_value': 0
    },
    {
        'code': 'ggt',
        'short_name': 'GGT',
        'name': 'GGT',
        'type': RESULT_SPEC_TYPE_FLOAT,
        'min_value': 0
    },
    {
        'code': 'glucose',
        'short_name': 'Gluc',
        'name': 'Glucose',
        'units': 'mmol/l',
        'type': RESULT_SPEC_TYPE_FLOAT,
        'min_value': 0
    },
    {
        'code': 'hb',
        'short_name': 'Hb',
        'name': 'HB',
        'units': 'g/l',
        'type': RESULT_SPEC_TYPE_FLOAT,
        'min_value': 0
    },
    {
        'code': 'hba1c',
        'short_name': 'HbA1C',
        'name': 'HbA1C',
        'type': RESULT_SPEC_TYPE_FLOAT,
        'min_value': 0
    },
    {
        'code': 'hco_3',
        'short_name': 'Bicarb',
        'name': 'Bicarbonate',
        'units': 'mmol/l',
        'type': RESULT_SPEC_TYPE_FLOAT,
        'min_value': 0
    },
    {
        'code': 'height',
        'short_name': 'Height',
        'name': 'Height',
        'units': 'cm',
        'type': RESULT_SPEC_TYPE_FLOAT,
        'min_value': 0
    },
    {
        'code': 'inr',
        'short_name': 'INR',
        'name': 'INR',
        'units': 'ratio',
        'type': RESULT_SPEC_TYPE_FLOAT,
        'min_value': 0
    },
    {
        'code': 'iron',
        'short_name': 'Iron',
        'name': 'Iron',
        'type': RESULT_SPEC_TYPE_FLOAT,
        'min_value': 0
    },
    {
        'code': 'ironsat',
        'short_name': 'Fe Sat',
        'name': 'Iron Saturation',
        'type': RESULT_SPEC_TYPE_FLOAT,
        'min_value': 0
    },
    {
        'code': 'ktv',
        'short_name': 'Kt/V',
        'name': 'Kt/V',
        'type': RESULT_SPEC_TYPE_FLOAT,
        'min_value': 0
    },
    {
        'code': 'lithium',
        'short_name': 'Lith',
        'name': 'Lithium',
        'type': RESULT_SPEC_TYPE_FLOAT,
        'min_value': 0
    },
    {
        'code': 'magnesium',
        'short_name': 'Mg',
        'name': 'Magnesium',
        'type': RESULT_SPEC_TYPE_FLOAT,
        'min_value': 0
    },
    {
        'code': 'pcr',
        'short_name': 'PCR',
        'name': 'Protein : Creatinine Ratio',
        'units': 'mg/mmol',
        'type': RESULT_SPEC_TYPE_FLOAT,
        'min_value': 0
    },
    {
        'code': 'phepku',
        'short_name': 'Phe',
        'name': 'Phenylalanine (for PKU)',
        'type': RESULT_SPEC_TYPE_FLOAT,
        'min_value': 0
    },
    {
        'code': 'phosphate',
        'short_name': 'Phos',
        'name': 'Phosphate',
        'units': 'mmol/l',
        'type': RESULT_SPEC_TYPE_FLOAT,
        'min_value': 0
    },
    {
        'code': 'platelets',
        'short_name': 'Plats',
        'name': 'Platelets',
        'type': RESULT_SPEC_TYPE_FLOAT,
        'min_value': 0
    },
    {
        'code': 'potassium',
        'short_name': 'Potassium',
        'name': 'Potassium',
        'units': 'mmol/l',
        'type': RESULT_SPEC_TYPE_FLOAT,
        'min_value': 0
    },
    {
        'code': 'pre_post_dialysis',
        'short_name': 'Pre/Post',
        'name': 'Pre/Post Dialysis',
        'type': RESULT_SPEC_TYPE_CODED_STRING,  # TODO
        'meta': True,
        'options': OrderedDict([
            ('PRE', 'Pre'),
            ('POST', 'Post'),
        ])
    },
    {
        'code': 'psa',
        'short_name': 'PSA',
        'name': 'PSA',
        'type': RESULT_SPEC_TYPE_FLOAT,
        'min_value': 0
    },
    {
        'code': 'pth',
        'short_name': 'PTH',
        'name': 'Parathyroid Hormone',
        'type': RESULT_SPEC_TYPE_FLOAT,
        'min_value': 0
    },
    {
        'code': 'sirolimus',
        'short_name': 'Siro',
        'name': 'Sirolimus',
        'type': RESULT_SPEC_TYPE_FLOAT,
        'min_value': 0
    },
    {
        'code': 'sodium',
        'short_name': 'Sodium',
        'name': 'Sodium',
        'units': 'mmol/l',
        'type': RESULT_SPEC_TYPE_FLOAT,
        'min_value': 0
    },
    {
        'code': 'tacrolimus',
        'short_name': 'Tacro',
        'name': 'Tacrolimus',
        'type': RESULT_SPEC_TYPE_FLOAT,
        'min_value': 0
    },
    {
        'code': 'testosterone',
        'short_name': 'Serum Testosterone',
        'name': 'Serum Testosterone',
        'type': RESULT_SPEC_TYPE_FLOAT,
        'min_value': 0
    },
    {
        'code': 'tg',
        'short_name': 'TG',
        'name': 'Triglycerides',
        'type': RESULT_SPEC_TYPE_FLOAT,
        'min_value': 0
    },
    {
        'code': 'transferrin',
        'short_name': 'Tferrin',
        'name': 'Transferrin',
        'type': RESULT_SPEC_TYPE_FLOAT,
        'min_value': 0
    },
    {
        'code': 'urate',
        'short_name': 'Urate',
        'name': 'Uric Acid',
        'units': 'mmol/l',
        'type': RESULT_SPEC_TYPE_FLOAT,
        'min_value': 0
    },
    {
        'code': 'urea',
        'short_name': 'Urea',
        'name': 'Urea',
        'units': 'mmol/l',
        'type': RESULT_SPEC_TYPE_FLOAT,
        'min_value': 0
    },
    {
        'code': 'urr',
        'short_name': 'URR',
        'name': 'Urea Reduction Ratio',
        'type': RESULT_SPEC_TYPE_FLOAT,
        'min_value': 0
    },
    {
        'code': 'vitd',
        'short_name': 'Vit D',
        'name': 'Vitamin D',
        'type': RESULT_SPEC_TYPE_FLOAT,
        'min_value': 0
    },
    {
        'code': 'wbc',
        'short_name': 'WBC',
        'name': 'White Blood Cell Count',
        'type': RESULT_SPEC_TYPE_FLOAT,
        'min_value': 0
    },
    {
        'code': 'weight',
        'short_name': 'Weight',
        'name': 'Weight',
        'units': 'kg',
        'type': RESULT_SPEC_TYPE_FLOAT,
        'min_value': 0
    }
]

RESULT_GROUP_SPECS = [
    {
        'code': 'urine',
        'name': 'Urine',
        'result_codes': [
            'acr',
            'pcr',
        ],
    },
    {
        'code': 'lft',
        'name': 'Liver Function Test',
        'result_codes': [
            'adjustedcalcium',
            'albumin',
            'alp',
            'alt',
            'bili',
            'ggt',
            'ast'
        ],
    },
    {
        'code': 'fats',
        'name': 'Fats',
        'result_codes': [
            'cholesterol',
            'tg',
        ],
    },
    {
        'code': 'drugs',
        'name': 'Drugs',
        'result_codes': [  # TODO order
            'ciclosporin',
            'sirolimus',
            'tacrolimus',
            'lithium',
        ],
    },
    {
        'code': 'ue',
        'name': 'Urea & Electrolytes',
        'result_codes': [
            'pre_post_dialysis',
            'sodium',
            'potassium',
            'hco_3',
            'urea',
            'creatinine',
            'egfr',
            'urate',
            'crp',
            'urr',
            'ktv',
        ],
    },
    {
        'code': 'heam',
        'name': 'Haematinics',
        'result_codes': [
            'ferritin',
            'iron',
            'ironsat',
            'transferrin',
        ],
    },
    {
        'code': 'dm',
        'name': 'Diabetes Monitoring',
        'result_codes': [
            'glucose',
            'hba1c',
        ],
    },
    {
        'code': 'fbc',
        'name': 'Full Blood Count',
        'result_codes': [
            'hb',
            'wbc',
            'platelets',
        ],
    },
    {
        'code': 'coag',
        'name': 'Coagulation',
        'result_codes': [
            'inr',
        ],
    },
    {
        'code': 'obv',
        'name': 'Observations',
        'result_codes': [  # TODO order
            'weight',
            'height',
            'bpdia',
            'bpsys',
        ]
    },
    {
        'code': 'bbc',
        'name': 'Bone Biochemistry',
        'result_codes': [  # TODO order
            'calcium',
            'magnesium',
            'phosphate',
            'vitd',
            'pth',
        ]
    },
    {
        'code': 'ham',
        'name': 'Hormones and Markers',
        'result_codes': [  # TODO order
            'phepku',
            'psa',
            'testosterone',
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
        result_spec.meta = x.get('meta', False)

        options = x.get('options')

        if options is not None:
            result_spec.options = [{'id': k, 'label': v} for k, v in options.items()]

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
