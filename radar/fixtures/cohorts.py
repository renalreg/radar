from radar.fixtures.utils import add
from radar.models.groups import Group, GROUP_TYPE, GroupPage
from radar.pages import PAGE
from radar.models.diagnoses import Diagnosis, GROUP_DIAGNOSIS_TYPE, GroupDiagnosis
from radar.models.forms import Form, GroupForm, GroupQuestionnaire


COHORTS = [
    {
        'code': 'NURTURECKD',
        'name': 'NURTuRE - CKD',
        'short_name': 'NURTuRE - CKD',
        'pages': [
            (PAGE.PRIMARY_DIAGNOSIS, 100),
            (PAGE.FAMILY_HISTORY, 300),
            (PAGE.DIAGNOSES, 400),
            (PAGE.MEDICATIONS, 800),
            (PAGE.RESULTS, 900),
            (PAGE.RENAL_PROGRESSION, 1000),
            (PAGE.DIALYSIS, 1100),
            (PAGE.TRANSPLANTS, 1200),
            (PAGE.QUESTIONNAIRES, 1300),
        ],
        'forms': [
            ('socio-economic', 200),
            ('diabetes', 500),
            ('diabetic-complications', 600),
            ('anthropometric', 700),
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
        'code': 'NURTUREINS',
        'name': 'NURTuRE - INS',
        'short_name': 'NURTuRE - INS',
        'pages': [
            (PAGE.QUESTIONNAIRES, 100),
        ],
        'questionnaires': [
            ('eq-5d-5l', 100),
            ('hads', 200),
            ('ipos', 300),
            ('6cit', 400),
            ('chu9d', 500),
            ('eq-5d-y', 600),
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

        for form_slug, weight in x.get('questionnaires', []):
            form = Form.query.filter(Form.slug == form_slug).one()

            group_questionnaire = GroupQuestionnaire()
            group_questionnaire.group = group
            group_questionnaire.form = form
            group_questionnaire.weight = weight
            add(group_questionnaire)
