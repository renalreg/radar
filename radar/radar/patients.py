from radar.permissions import has_view_demographics_permission
from radar.serializers.core import Empty


class PatientProxy(object):
    def __init__(self, patient, user):
        self.patient = patient
        self.user = user
        self.demographics_permission = has_view_demographics_permission(patient, user)

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
    def cohorts(self):
        return [x.cohort for x in self.cohort_patients]

    @property
    def cohort_patients(self):
        # if self.user.is_admin:
        #     return self.patient.cohort_patients
        #
        # organisations = intersect_patient_and_user_organisations(self.patient, self.user)
        #
        # if organisations:
        #     return self.patient.cohort_patients
        # else:
        #     return intersect_patient_and_user_cohorts(self.patient, self.user, patient_membership=True)

        return self.patient.cohort_patients

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
