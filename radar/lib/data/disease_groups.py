from radar.lib.database import db
from radar.models import DiseaseGroup, DiseaseGroupFeature, LabGroupDefinition, DiseaseGroupLabGroupDefinition

# TODO
DISEASE_GROUPS = [
    {
        'name': 'SRNS',
        'features': [
            ('DEMOGRAPHICS', 0),
            ('GENETICS', 1),
            ('RENAL_IMAGING', 2),
            ('SALT_WASTING_CLINICAL_FEATURES', 3),
        ],
        'lab_group_definitions': [
            ('TEST', 4),
        ],
    },
    {
        'name': 'MPGN',
        'features': [
            ('DEMOGRAPHICS', 0),
            ('GENETICS', 1),
            ('RENAL_IMAGING', 2),
            ('SALT_WASTING_CLINICAL_FEATURES', 3),
        ],
        'lab_group_definitions': [
            ('TEST', 4),
        ],
    },
    {
        'name': 'Salt Wasting',
        'features': [
            ('DEMOGRAPHICS', 0),
            ('GENETICS', 1),
            ('RENAL_IMAGING', 2),
            ('SALT_WASTING_CLINICAL_FEATURES', 3),
        ],
        'lab_group_definitions': [
            ('TEST', 4),
        ],
    }
]


def create_disease_groups():
    for x in DISEASE_GROUPS:
        disease_group = DiseaseGroup(name=x['name'])
        db.session.add(disease_group)

        for name, weight in x['features']:
            disease_group_feature = DiseaseGroupFeature(
                disease_group=disease_group,
                name=name,
                weight=weight
            )
            db.session.add(disease_group_feature)

        for code, weight in x['lab_group_definitions']:
            lab_group_definition = LabGroupDefinition.query.filter(LabGroupDefinition.code == code).one()

            disease_group_lab_group_definition = DiseaseGroupLabGroupDefinition(
                disease_group=disease_group,
                lab_group_definition=lab_group_definition,
                weight=weight,
            )
            db.session.add(disease_group_lab_group_definition)
