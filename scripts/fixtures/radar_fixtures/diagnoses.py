from radar.models.diagnoses import GroupDiagnosis, GROUP_DIAGNOSIS_TYPE, Diagnosis
from radar.models.groups import Group, GROUP_TYPE

from radar_fixtures.utils import add

DIAGNOSES = [
    'ADPKD',
    'ARPKD',
    'Abdominal Enlargement',
    'Anorectal Varices',
    'Anxiety',
    'Arachnoid Cysts',
    'Ascites',
    'Bile Duct Cysts',
    'Cardiomyopathy',
    'Cerebral Haemorrhage - Mitral Valve Prolapse',
    'Cholangitis - Acute',
    'Cholangitis - Recurrent',
    'Depression',
    'Gastric Varices',
    'Haematuria',
    'Hepatic Fibrosis',
    'Hypertension',
    'Inguinal Hernia',
    'Intracranial Aneurysm',
    'Left Ventricular Hypertrophy',
    'Liver Cyst Infection',
    'Lung Disease - Chronic',
    'Oesophageal Variceal Haemorrhage',
    'Oesophageal Varices',
    'Pancreatic Cysts',
    'Polycystic Liver Disease',
    'Portal Hypertension',
    'Renal Cyst - Infection',
    'Renal Cyst Haemorrhage',
    'Renal Stones',
    'Seminal Vesicle Cysts',
    'Spleen - Palpable - Splenomegaly',
    'UTI - Urinary Tract Infection',
]

GROUP_DIAGNOSES = {
    'ADPKD': [
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
    ],
    'ARPKD': [
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
