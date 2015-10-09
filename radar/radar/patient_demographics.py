from radar.permissions import has_view_demographics_permission
from radar.serializers.core import Empty


class PatientDemographicsProxy(object):
    def __init__(self, demographics, user):
        self.demographics = demographics
        self.user = user
        self.demographics_permission = has_view_demographics_permission(demographics.patient, user)

    @property
    def first_name(self):
        if self.demographics_permission:
            return self.demographics.first_name
        else:
            return Empty

    @property
    def last_name(self):
        if self.demographics_permission:
            return self.demographics.last_name
        else:
            return Empty

    @property
    def date_of_birth(self):
        if self.demographics_permission:
            return self.demographics.date_of_birth
        else:
            return Empty

    @property
    def year_of_birth(self):
        return self.demographics.date_of_birth.year

    @property
    def date_of_death(self):
        if self.demographics_permission:
            return self.demographics.date_of_death
        else:
            return Empty

    @property
    def year_of_death(self):
        if self.demographics.date_of_death is not None:
            return self.demographics.date_of_death.year
        else:
            return None

    @property
    def home_number(self):
        if self.demographics_permission:
            return self.demographics.home_number
        else:
            return Empty

    @property
    def work_number(self):
        if self.demographics_permission:
            return self.demographics.work_number
        else:
            return Empty

    @property
    def mobile_number(self):
        if self.demographics_permission:
            return self.demographics.mobile_number
        else:
            return Empty

    @property
    def email_address(self):
        if self.demographics_permission:
            return self.demographics.email_address
        else:
            return Empty

    def __getattr__(self, item):
        return getattr(self.demographics, item)
