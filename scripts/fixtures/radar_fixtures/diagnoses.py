from radar.models.diagnoses import GroupDiagnosis, GROUP_DIAGNOSIS_TYPE, Diagnosis
from radar.models.groups import Group, GROUP_TYPE

from radar_fixtures.utils import add

DIAGNOSES = [
    'Blindness',
    'Deafness',
    'Diabetes',
    'Hepatitis B',
    'Hepatitis C',
]

GROUP_DIAGNOSES = {
    'BONEITIS': [
        ('Blindness', GROUP_DIAGNOSIS_TYPE.PRIMARY),
        ('Deafness', GROUP_DIAGNOSIS_TYPE.PRIMARY),
        ('Diabetes', GROUP_DIAGNOSIS_TYPE.SECONDARY),
    ],
    'CIRCUSITIS': [
        ('Hepatitis B', GROUP_DIAGNOSIS_TYPE.PRIMARY),
        ('Hepatitis C', GROUP_DIAGNOSIS_TYPE.PRIMARY),
        ('Diabetes', GROUP_DIAGNOSIS_TYPE.SECONDARY),
    ]
}


def create_diagnoses():
    diagnosis_map = {}

    for name in DIAGNOSES:
        diagnosis = Diagnosis()
        diagnosis.name = name
        add(diagnosis)
        diagnosis_map[name] = diagnosis

    for code, diagnoses in GROUP_DIAGNOSES.items():
        group = Group.query.filter(Group.code == code, Group.type == GROUP_TYPE.COHORT).one()

        for diagnosis_name, group_diagnosis_type in diagnoses:
            diagnosis = diagnosis_map[diagnosis_name]

            group_diagnosis = GroupDiagnosis()
            group_diagnosis.group = group
            group_diagnosis.diagnosis = diagnosis
            group_diagnosis.type = group_diagnosis_type
            add(group_diagnosis)
