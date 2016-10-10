from radar.models.diagnoses import Diagnosis
from radar.fixtures.utils import add

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


def create_diagnoses():
    for name in DIAGNOSES:
        diagnosis = Diagnosis()
        diagnosis.name = name
        add(diagnosis)
