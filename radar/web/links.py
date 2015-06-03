from functools import partial
from flask import url_for
from jinja2 import contextfunction
from radar.lib import features


class PatientLink(object):
    def __init__(self, patient, name, endpoint, patient_page):
        self.patient = patient
        self.name = name
        self.endpoint = endpoint
        self.patient_page = patient_page

    def text(self):
        return self.name

    def url(self):
        return url_for(self.endpoint, patient_id=self.patient.id)

    @contextfunction
    def is_active(self, context):
        return context.vars.get('current_patient_page') == self.patient_page

    @classmethod
    def partial(cls, name, endpoint, patient_page):
        return partial(cls, name=name, endpoint=endpoint, patient_page=patient_page)


class DiseaseGroupLink(object):
    def __init__(self, patient, disease_group, name, endpoint, patient_page):
        self.patient = patient
        self.disease_group = disease_group
        self.name = name
        self.endpoint = endpoint
        self.patient_page = patient_page

    def text(self):
        return self.name

    def url(self):
        return url_for(self.endpoint, patient_id=self.patient.id, disease_group_id=self.disease_group.id)

    @contextfunction
    def is_active(self, context):
        return (
            context.vars.get('current_patient_page') == self.patient_page and
            context.vars.get('current_patient_disease_group') == self.disease_group
        )

    @classmethod
    def partial(cls, name, endpoint, patient_page):
        return partial(cls, name=name, endpoint=endpoint, patient_page=patient_page)


class LabGroupLink(object):
    def __init__(self, patient, lab_group_definition):
        self.patient = patient
        self.lab_group_definition = lab_group_definition

    def text(self):
        return self.lab_group_definition.name

    def url(self):
        return url_for(
            'lab_results.view_lab_result_list',
            patient_id=self.patient.id,
            lab_group_definition_id=self.lab_group_definition.id,
        )

    @contextfunction
    def is_active(self, context):
        return (
            context.vars.get('current_patient_page') == 'lab_results' and
            context.vars.get('current_lab_group_definition') == self.lab_group_definition
        )


# Patient links
demographics_link = PatientLink.partial('Demographics', 'patients.view_demographics_list', 'demographics')
medications_link = PatientLink.partial('Medications', 'medications.view_medication_list', 'medications')
lab_results_link = PatientLink.partial('Lab Results', 'lab_results.view_lab_result_list', 'lab_results')
hospitalisations_link = PatientLink.partial('Hospitalisations', 'hospitalisations.view_hospitalisation_list', 'hospitalisations')
pathology_link = PatientLink.partial('Pathology', 'pathology.view_pathology_list', 'pathology')
transplants_link = PatientLink.partial('Transplants', 'transplants.view_transplant_list', 'transplants')
dialysis_link = PatientLink.partial('Dialysis', 'dialysis.view_dialysis_list', 'dialysis')
plasmapheresis_link = PatientLink.partial('Plasmapheresis', 'plasmapheresis.view_plasmapheresis_list', 'plasmapheresis')
renal_imaging_link = PatientLink.partial('Renal Imaging', 'renal_imaging.view_renal_imaging_list', 'renal_imaging')
salt_wasting_clinical_features_link = PatientLink.partial('Clinical Features', 'salt_wasting.view_clinical_features', 'salt_wasting_clinical_features')

# Disease group links
genetics_link = DiseaseGroupLink.partial('Genetics', 'genetics.view_genetics', 'genetics')

PATIENT_LINKS = [
    demographics_link,
    medications_link,
    lab_results_link,
    hospitalisations_link,
    pathology_link,
    transplants_link,
    dialysis_link,
    plasmapheresis_link,
]

FEATURE_TO_PATIENT_LINK = {
    features.RENAL_IMAGING: renal_imaging_link,
    features.SALT_WASTING_CLINICAL_FEATURES: salt_wasting_clinical_features_link,
}

FEATURE_TO_DISEASE_GROUP_LINK = {
    features.GENETICS: genetics_link,
}


def get_patient_links(patient):
    links = []

    for x in PATIENT_LINKS:
        links.append(x(patient))

    return links


def get_disease_group_links(patient, disease_group):
    links = []

    for x in disease_group.features:
        link = FEATURE_TO_PATIENT_LINK.get(x.name)

        if link is not None:
            links.append((x.weight, link(patient)))
            continue

        link = FEATURE_TO_DISEASE_GROUP_LINK.get(x.name)

        if link is not None:
            links.append((x.weight, link(patient, disease_group)))
            continue

    for x in disease_group.disease_group_lab_group_definitions:
        link = LabGroupLink(patient, x.lab_group_definition)
        links.append((x.weight, link))

    links = [x[1] for x in sorted(links)]

    return links
