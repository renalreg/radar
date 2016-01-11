from radar.permissions import has_permission_for_patient
from radar.serializers.core import Empty
from radar.roles import PERMISSIONS


class PatientProxy(object):
    def __init__(self, patient, user):
        self.patient = patient
        self.user = user
        self.demographics_permission = has_permission_for_patient(user, patient, PERMISSIONS.VIEW_DEMOGRAPHICS)

    @property
    def first_name(self):
        if self.demographics_permission:
            return self.patient.first_name
        else:
            return Empty

    @property
    def last_name(self):
        if self.demographics_permission:
            return self.patient.last_name
        else:
            return Empty

    @property
    def date_of_birth(self):
        if self.demographics_permission:
            return self.patient.date_of_birth
        else:
            return Empty

    @property
    def year_of_birth(self):
        if self.patient.date_of_birth is not None:
            return self.patient.date_of_birth.year
        else:
            return None

    @property
    def year_of_death(self):
        if self.patient.date_of_death is not None:
            return self.patient.date_of_death.year
        else:
            return None

    def __getattr__(self, item):
        return getattr(self.patient, item)
