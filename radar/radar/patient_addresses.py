from radar.permissions import has_permission_for_patient
from radar.serializers.core import Empty
from radar.roles import PERMISSION


class PatientAddressProxy(object):
    def __init__(self, address, user):
        self.address = address
        self.user = user
        self.demographics_permission = has_permission_for_patient(user, address.patient, PERMISSION.VIEW_DEMOGRAPHICS)

    @property
    def address_1(self):
        if self.demographics_permission:
            return self.address.address_1
        else:
            return Empty

    @property
    def address_2(self):
        if self.demographics_permission:
            return self.address.address_2
        else:
            return Empty

    @property
    def address_3(self):
        if self.demographics_permission:
            return self.address.address_3
        else:
            return Empty

    @property
    def address_4(self):
        if self.demographics_permission:
            return self.address.address_4
        else:
            return Empty

    @property
    def postcode(self):
        postcode = self.address.postcode

        if self.demographics_permission:
            return postcode
        else:
            # Return the first part of the postcode
            # Postcodes from the database should have a space but limit to 4 characters just in case
            return postcode.split(' ')[0][:4]

    def __getattr__(self, item):
        return getattr(self.address, item)
