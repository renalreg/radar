class BasePermission(object):
    def has_permission(self):
        return True

    def has_object_permission(self, obj):
        return True


class PatientDataPermission(BasePermission):
    def has_permission(self):
        # TODO
        return True

    def has_object_permission(self, obj):
        # TODO
        return True


class FacilityDataPermission(BasePermission):
    def has_permission(self):
        # TODO
        return True

    def has_object_permission(self, obj):
        # TODO
        return True
