from radar.fixtures.utils import add
from radar.models.diagnoses import Diagnosis, GroupDiagnosis
from radar.models.forms import Form, GroupForm, GroupQuestionnaire
from radar.models.groups import (
    Group,
    GroupPage,
    GROUP_CODE_RADAR,
    GROUP_CODE_NURTURE,
    GROUP_CODE_NHS,
    GROUP_CODE_CHI,
    GROUP_CODE_UKRR,
    GROUP_CODE_HSC,
    GROUP_CODE_UKRDC,
    GROUP_CODE_NHSBT,
    GROUP_CODE_BAPN,
    GROUP_TYPE,
)
from radar.pages import PAGE


batches = [
    [
        {
            'type': GROUP_TYPE.SYSTEM,
            'code': GROUP_CODE_RADAR,
            'name': 'RaDaR',
            'pages': [
                (PAGE.DEMOGRAPHICS, 100),
                (PAGE.CONSULTANTS, 200),
                (PAGE.COHORTS, 300),
                (PAGE.HOSPITALS, 400),
            ],
        },
        {
            'type': GROUP_TYPE.SYSTEM,
            'code': GROUP_CODE_NURTURE,
            'name': 'NURTuRE',
            'pages': [
                (PAGE.DEMOGRAPHICS, 100),
                (PAGE.CONSULTANTS, 200),
                (PAGE.COHORTS, 300),
                (PAGE.HOSPITALS, 400),
            ],
        }
    ],
    [
        {
            'type': GROUP_TYPE.OTHER,
            'code': GROUP_CODE_NHS,
            'name': 'NHS',
            'is_recruitment_number_group': True
        },
        {
            'type': GROUP_TYPE.OTHER,
            'code': GROUP_CODE_CHI,
            'name': 'CHI',
            'is_recruitment_number_group': True
        },
        {
            'type': GROUP_TYPE.OTHER,
            'code': GROUP_CODE_HSC,
            'name': 'HSC',
            'is_recruitment_number_group': True
        },
        {
            'type': GROUP_TYPE.OTHER,
            'code': GROUP_CODE_UKRR,
            'name': 'UK Renal Registry',
        },
        {
            'type': GROUP_TYPE.OTHER,
            'code': GROUP_CODE_UKRDC,
            'name': 'UKRDC',
        },
        {
            'type': GROUP_TYPE.OTHER,
            'code': GROUP_CODE_NHSBT,
            'name': 'NHS Blood and Transplant',
        },
        {
            'type': GROUP_TYPE.OTHER,
            'code': GROUP_CODE_BAPN,
            'name': 'BAPN',
        },
    ],
    [
        {
            'type': GROUP_TYPE.HOSPITAL,
            'code': 'EAST',
            'name': 'East Hampton Hospital',
        },
        {
            'type': GROUP_TYPE.HOSPITAL,
            'code': 'HOLBY',
            'name': 'Holby City Hospital',
        },
    ],
    [
        {
            'type': GROUP_TYPE.COHORT,
            'code': 'NURTURECKD',
            'name': 'NURTuRE - CKD',
            'short_name': 'NURTuRE - CKD',
            'parent_group': (GROUP_TYPE.SYSTEM, GROUP_CODE_NURTURE),
            'pages': [
                (PAGE.PRIMARY_DIAGNOSIS, 100),
                (PAGE.DIAGNOSES, 400),
                (PAGE.MEDICATIONS, 800),
                (PAGE.RESULTS, 900),
                (PAGE.PATHOLOGY, 950),
                (PAGE.RENAL_PROGRESSION, 1000),
                (PAGE.DIALYSIS, 1100),
                (PAGE.TRANSPLANTS, 1200),
                (PAGE.QUESTIONNAIRES, 1300),
            ],
            'forms': [
                ('socio-economic', 200),
                ('family-history', 500),
                ('diabetic-complications', 600),
                ('anthropometrics', 700),
                ('samples', 1250),
            ],
            'questionnaires': [
                ('eq-5d-5l', 100),
                ('hads', 200),
                ('ipos', 300),
                ('6cit', 400),
                ('chu9d', 500),
                ('eq-5d-y', 600),
            ]
        },
        {
            'type': GROUP_TYPE.COHORT,
            'code': 'NURTUREINS',
            'name': 'NURTuRE - INS',
            'short_name': 'NURTuRE - INS',
            'parent_group': (GROUP_TYPE.SYSTEM, GROUP_CODE_NURTURE),
            'pages': [
                (PAGE.QUESTIONNAIRES, 100),
            ],
            'forms': [
                ('samples', 50),
            ],
            'questionnaires': [
                ('eq-5d-5l', 100),
                ('hads', 200),
                ('ipos', 300),
                ('6cit', 400),
                ('chu9d', 500),
                ('eq-5d-y', 600),
            ]
        },
        {
            'type': GROUP_TYPE.COHORT,
            'code': 'INS',
            'name': 'Idiopathic Nephrotic Syndrome',
            'short_name': 'INS',
            'parent_group': (GROUP_TYPE.SYSTEM, GROUP_CODE_RADAR),
            'pages': [
                (PAGE.PRIMARY_DIAGNOSIS, 100),
                (PAGE.GENETICS, 200),
                (PAGE.FAMILY_HISTORY, 300),
                (PAGE.DIAGNOSES, 400),
                (PAGE.PATHOLOGY, 500),
                (PAGE.INS_CLINICAL_PICTURES, 600),
                (PAGE.RESULTS, 700),
                (PAGE.MEDICATIONS, 800),
                (PAGE.INS_RELAPSES, 900),
                (PAGE.DIALYSIS, 1000),
                (PAGE.PLASMAPHERESIS, 1100),
                (PAGE.TRANSPLANTS, 1200),
                (PAGE.HOSPITALISATIONS, 1300),
            ],
        },
    ]
]


def create_groups():
    for groups in batches:
        for x in groups:
            group = Group()
            group.type = x['type']
            group.code = x['code']
            group.name = x['name']
            group.short_name = x.get('short_name', group.name)
            group.is_recruitment_number_group = x.get('is_recruitment_number_group', False)

            if 'parent_group' in x:
                parent_type, parent_code = x['parent_group']
                parent_group = Group.query.filter(Group.type == parent_type, Group.code == parent_code).one()
                group.parent_group = parent_group

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

            for form_slug, weight in x.get('questionnaires', []):
                form = Form.query.filter(Form.slug == form_slug).one()

                group_questionnaire = GroupQuestionnaire()
                group_questionnaire.group = group
                group_questionnaire.form = form
                group_questionnaire.weight = weight
                add(group_questionnaire)
