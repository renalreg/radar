from radar.permissions import can_view_demographics
from radar.serializers.core import Empty


class PatientAddressProxy(object):
    def __init__(self, address, user):
        self.address = address
        self.user = user
        self.demographics_permission = can_view_demographics(user, address.patient)

    @property
    def address1(self):
        if self.demographics_permission:
            return self.address.address1
        else:
            return Empty

    @property
    def address2(self):
        if self.demographics_permission:
            return self.address.address2
        else:
            return Empty

    @property
    def address3(self):
        if self.demographics_permission:
            return self.address.address3
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
