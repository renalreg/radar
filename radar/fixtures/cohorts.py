from radar.fixtures.utils import add
from radar.models.groups import Group, GROUP_TYPE, GroupPage
from radar.pages import PAGE
from radar.models.diagnoses import Diagnosis, GROUP_DIAGNOSIS_TYPE, GroupDiagnosis
from radar.models.forms import Form, GroupForm, GroupQuestionnaire


COHORTS = [
    {
        'code': 'BONEITIS',
        'name': 'Bone-itis',
        'short_name': 'Bone-itis',
        'pages': [
            (PAGE.PRIMARY_DIAGNOSIS, 100),
            (PAGE.DIAGNOSES, 200),
        ],
    },
    {
        'code': 'CIRCUSITIS',
        'name': 'Circusitis',
        'short_name': 'Circusitis',
        'pages': [
            (PAGE.PRIMARY_DIAGNOSIS, 100),
            (PAGE.DIAGNOSES, 200),
        ],
    },
    {
        'code': 'ADTKD',
        'name': 'Autosomal Dominant Tubulointerstitial Kidney Disease (FUAN)',
        'short_name': 'ADTKD (FUAN)',
        'pages': [
            (PAGE.PRIMARY_DIAGNOSIS, 100),
            (PAGE.DIAGNOSES, 200),
            (PAGE.GENETICS, 300),
            (PAGE.FAMILY_HISTORY, 400),
            (PAGE.FUAN_CLINICAL_PICTURES, 500),
            (PAGE.RESULTS, 600),
            (PAGE.DIALYSIS, 700),
            (PAGE.TRANSPLANTS, 800),
        ]
    },
    {
        'code': 'ADPKD',
        'name': 'Autosomal Dominant Polycystic Kidney Disease',
        'short_name': 'ADPKD',
        'pages': [
            (PAGE.PRIMARY_DIAGNOSIS, 100),
            (PAGE.DIAGNOSES, 200),
            (PAGE.GENETICS, 300),
            (PAGE.FAMILY_HISTORY, 400),
            (PAGE.RENAL_IMAGING, 500),
            (PAGE.LIVER_IMAGING, 600),
            (PAGE.LIVER_DISEASES, 700),
            (PAGE.RESULTS, 800),
            (PAGE.TRANSPLANTS, 900),
            (PAGE.LIVER_TRANSPLANTS, 1000),
        ],
        'diagnoses': [
            ('ADPKD', GROUP_DIAGNOSIS_TYPE.PRIMARY),
            ('Abdominal Enlargement', GROUP_DIAGNOSIS_TYPE.SECONDARY),
            ('Anxiety', GROUP_DIAGNOSIS_TYPE.SECONDARY),
            ('Arachnoid Cysts', GROUP_DIAGNOSIS_TYPE.SECONDARY),
            ('Cardiomyopathy', GROUP_DIAGNOSIS_TYPE.SECONDARY),
            ('Cerebral Haemorrhage - Mitral Valve Prolapse', GROUP_DIAGNOSIS_TYPE.SECONDARY),
            ('Depression', GROUP_DIAGNOSIS_TYPE.SECONDARY),
            ('Haematuria', GROUP_DIAGNOSIS_TYPE.SECONDARY),
            ('Hypertension', GROUP_DIAGNOSIS_TYPE.SECONDARY),
            ('Inguinal Hernia', GROUP_DIAGNOSIS_TYPE.SECONDARY),
            ('Intracranial Aneurysm', GROUP_DIAGNOSIS_TYPE.SECONDARY),
            ('Left Ventricular Hypertrophy', GROUP_DIAGNOSIS_TYPE.SECONDARY),
            ('Liver Cyst Infection', GROUP_DIAGNOSIS_TYPE.SECONDARY),
            ('Pancreatic Cysts', GROUP_DIAGNOSIS_TYPE.SECONDARY),
            ('Polycystic Liver Disease', GROUP_DIAGNOSIS_TYPE.SECONDARY),
            ('Renal Cyst - Infection', GROUP_DIAGNOSIS_TYPE.SECONDARY),
            ('Renal Cyst Haemorrhage', GROUP_DIAGNOSIS_TYPE.SECONDARY),
            ('Renal Stones', GROUP_DIAGNOSIS_TYPE.SECONDARY),
            ('Seminal Vesicle Cysts', GROUP_DIAGNOSIS_TYPE.SECONDARY),
            ('UTI - Urinary Tract Infection', GROUP_DIAGNOSIS_TYPE.SECONDARY),
        ]
    },
    {
        'code': 'ARPKD',
        'name': 'Autosomal Recessive Polycystic Kidney Disease',
        'short_name': 'ARPKD',
        'pages': [
            (PAGE.PRIMARY_DIAGNOSIS, 100),
            (PAGE.DIAGNOSES, 200),
            (PAGE.GENETICS, 300),
            (PAGE.FAMILY_HISTORY, 400),
            (PAGE.FETAL_ULTRASOUNDS, 500),
            (PAGE.RENAL_IMAGING, 600),
            (PAGE.LIVER_IMAGING, 700),
            (PAGE.LIVER_DISEASES, 800),
            (PAGE.RESULTS, 900),
            (PAGE.NUTRITION, 1000),
            (PAGE.LIVER_TRANSPLANTS, 1100),
            (PAGE.NEPHRECTOMIES, 1200),
        ],
        'diagnoses': [
            ('ARPKD', GROUP_DIAGNOSIS_TYPE.PRIMARY),
            ('Anorectal Varices', GROUP_DIAGNOSIS_TYPE.SECONDARY),
            ('Ascites', GROUP_DIAGNOSIS_TYPE.SECONDARY),
            ('Bile Duct Cysts', GROUP_DIAGNOSIS_TYPE.SECONDARY),
            ('Cholangitis - Acute', GROUP_DIAGNOSIS_TYPE.SECONDARY),
            ('Cholangitis - Recurrent', GROUP_DIAGNOSIS_TYPE.SECONDARY),
            ('Gastric Varices', GROUP_DIAGNOSIS_TYPE.SECONDARY),
            ('Hepatic Fibrosis', GROUP_DIAGNOSIS_TYPE.SECONDARY),
            ('Lung Disease - Chronic', GROUP_DIAGNOSIS_TYPE.SECONDARY),
            ('Oesophageal Variceal Haemorrhage', GROUP_DIAGNOSIS_TYPE.SECONDARY),
            ('Oesophageal Varices', GROUP_DIAGNOSIS_TYPE.SECONDARY),
            ('Portal Hypertension', GROUP_DIAGNOSIS_TYPE.SECONDARY),
            ('Spleen - Palpable - Splenomegaly', GROUP_DIAGNOSIS_TYPE.SECONDARY),
        ]
    },
    {
        'code': 'NURTURE',
        'name': 'NURTuRE',
        'short_name': 'NURTuRE',
        'pages': [
            (PAGE.QUESTIONNAIRES, 100),
        ],
        'forms': [
            ('anthropometric', 200),
            ('diabetes', 300),
            ('diabetic-complications', 400),
            ('socio-economic', 500),
        ],
        'questionnaires': [
            '6cit',
            'chu9d',
            'eq-5d-5l',
            'eq-5d-y',
            'hads',
            'ipos',
            'pam',
        ]
    }
]


def create_cohorts():
    for x in COHORTS:
        group = Group()
        group.type = GROUP_TYPE.COHORT
        group.code = x['code']
        group.name = x['name']
        group.short_name = x['short_name']
        group.pages = x['pages']
        add(group)

        for diagnosis_name, diagnosis_type in x.get('diagnoses', []):
            diagnosis = Diagnosis.query.filter(Diagnosis.name == diagnosis_name).one()

            group_diagnosis = GroupDiagnosis()
            group_diagnosis.group = group
            group_diagnosis.diagnosis = diagnosis
            group_diagnosis.type = diagnosis_type
            add(group_diagnosis)

        for page, weight in x.get('pages', []):
            group_page = GroupPage()
            group_page.group = group
            group_page.page = page
            group_page.weight = weight
            add(group_page)

        for form_slug, weight in x.get('forms', []):
            form = Form.query.filter(Form.slug == form_slug).one()

            group_form = GroupForm()
            group_form.group = group
            group_form.form = form
            group_form.weight = weight
            add(group_form)

        for form_slug in x.get('questionnaires', []):
            form = Form.query.filter(Form.slug == form_slug).one()

            group_questionnaire = GroupQuestionnaire()
            group_questionnaire.group = group
            group_questionnaire.form = form
            add(group_questionnaire)
