from radar_fixtures.validation import validate_and_add
from radar.models.diagnoses import GroupDiagnosis, GROUP_DIAGNOSIS_TYPE, Diagnosis
from radar.models.groups import Group, GROUP_TYPE

DIAGNOSES = [
    'Blindness',
    'Deafness',
    'Diabetes',
    'Hepatitis B',
    'Hepatitis C',
]

GROUP_DIAGNOSES = {
    'BONEITIS': [
        ('Blindness', GROUP_DIAGNOSIS_TYPE.CHILD),
        ('Deafness', GROUP_DIAGNOSIS_TYPE.CHILD),
        ('Diabetes', GROUP_DIAGNOSIS_TYPE.SIGNIFICANT),
    ],
    'CIRCUSITIS': [
        ('Hepatitis B', GROUP_DIAGNOSIS_TYPE.CHILD),
        ('Hepatitis C', GROUP_DIAGNOSIS_TYPE.CHILD),
        ('Diabetes', GROUP_DIAGNOSIS_TYPE.SIGNIFICANT),
    ]
}


def create_diagnoses():
    diagnosis_map = {}

    for name in DIAGNOSES:
        diagnosis = Diagnosis()
        diagnosis.name = name
        validate_and_add(diagnosis)
        diagnosis_map[name] = diagnosis

    for code, diagnoses in GROUP_DIAGNOSES.items():
        group = Group.query.filter(Group.code == code, Group.type == GROUP_TYPE.COHORT).one()

        for diagnosis_name, group_diagnosis_type in diagnoses:
            diagnosis = diagnosis_map[diagnosis_name]

            group_diagnosis = GroupDiagnosis()
            group_diagnosis.group = group
            group_diagnosis.diagnosis = diagnosis
            group_diagnosis.type = group_diagnosis_type
            validate_and_add(group_diagnosis)
