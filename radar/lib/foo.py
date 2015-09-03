from collections import OrderedDict
import copy
import six
from radar.lib.permissions import intersect_units
from radar.lib.serializers import ValidationError
from radar.models import Dialysis


def with_context(f):
    f.with_context = True
    return f


@with_context
def required(value):
    if value is None:
        raise ValidationError('This field is required.')


def optional(value):
    if value is None:
        raise SkipField()


class SkipField(Exception):
    pass


class Field(object):
    _creation_counter = 0

    def __init__(self, chain=None):
        # Keep track of field declaration order
        self._creation_counter = Field._creation_counter
        Field._creation_counter += 1

        if chain is None:
            chain = []

        self.chain = chain
        self.field_name = None

    def bind(self, field_name):
        self.field_name = field_name

    def set_value(self, obj, value):
        return setattr(obj, self.field_name, value)

    def get_value(self, obj):
        return getattr(obj, self.field_name)

    def get_validators(self):
        return self.chain

    def validate(self, ctx, obj):
        return obj

    def run_validators(self, value, context):
        validators = self.get_validators()

        for validator in validators:
            validator(value)

    def get_context(self, obj, ctx):
        return {}

    def run_validation(self, value, ctx=None):
        new_ctx = {}

        if ctx is not None:
            new_ctx.update(ctx)

        new_ctx.update(self.get_context(value, new_ctx))

        self.run_validators(value, new_ctx)

        value = self.validate(new_ctx, value)

        return value


class ValidatorMetaclass(type):
    def __new__(cls, name, bases, attrs):
        attrs['_declared_fields'] = cls.get_fields(bases, attrs)
        return super(ValidatorMetaclass, cls).__new__(cls, name, bases, attrs)

    @classmethod
    def get_fields(cls, bases, attrs):
        fields = []

        # Get the fields declared on this class
        for field_name, obj in list(attrs.items()):
            if isinstance(obj, Field):
                fields.append((field_name, attrs.pop(field_name)))

        # Sort the fields in the order they were declared
        fields.sort(key=lambda x: x[1]._creation_counter)

        # Sort the fields in the order they were declared
        fields.sort(key=lambda x: x[1]._creation_counter)

        # Loop in reverse to maintain correct field ordering
        for base in reversed(bases):
            if hasattr(base, '_declared_fields'):
                # Copy fields from another serializer
                # Parent serializer's fields go first
                fields = list(base._declared_fields.items()) + fields
            else:
                # Copy fields from mixins
                mixin_fields = []

                for field_name, obj in base.__dict__.items():
                    if isinstance(obj, Field):
                        mixin_fields.append((field_name, obj))

                # Sort the mixin fields in the order they were declared
                mixin_fields.sort(key=lambda x: x[1]._creation_counter)

                # Add the mixin fields
                fields = mixin_fields + fields

        return OrderedDict(fields)


@six.add_metaclass(ValidatorMetaclass)
class Validator(Field):
    def __init__(self, *args, **kwargs):
        super(Validator, self).__init__(*args, **kwargs)
        self._fields = None

    @property
    def fields(self):
        if self._fields is None:
            self._fields = self.get_fields()

        return self._fields

    def get_fields(self):
        # Deep copy the fields before binding them
        fields = copy.deepcopy(self._declared_fields)

        for field_name, field in fields.items():
            field.bind(field_name)

        return fields

    def run_validation(self, value, ctx=None):
        errors = {}

        new_ctx = {}

        if ctx is not None:
            new_ctx.update(ctx)

        new_ctx.update(self.get_context(value, new_ctx))

        for field_name, field in self.fields.items():
            field_value = getattr(value, field_name)

            try:
                field_value = field.run_validation(field_value, new_ctx)

                validate_method = getattr(self, 'validate_' + field.field_name, None)

                if validate_method is not None:
                    field_value = validate_method(new_ctx, field_value)
            except ValidationError as e:
                errors[field.field_name] = e.detail
            except SkipField:
                pass
            else:
                setattr(value, field_name, field_value)

        if errors:
            raise ValidationError(errors)

        self.run_validators(value, ctx)

        value = self.validate(new_ctx, value)

        return value


class PatientMixin(object):
    patient = Field(chain=[required])

    def get_context(self, obj, ctx):
        ctx = super(PatientMixin, self).get_context(obj, ctx)

        if obj.patient is not None:
            ctx['patient'] = obj.patient

        return ctx

    def validate(self, ctx, obj):
        user = ctx['user']

        if user.is_admin:
            return

        patient = obj.patient

        unit_users = intersect_units(patient, user, user_membership=True)

        if not any(x.has_edit_patient_permission for x in unit_users):
            raise ValidationError({'patient': "You don't have permission for this patient."})


class FacilityMixin(object):
    facility = Field(chain=[required])

    def validate(self, ctx, obj):
        user = ctx['user']

        if user.is_admin:
            return

        facility = obj.facility

        if not facility.is_internal:
            raise ValidationError({'facility': "You don't have permission for this facility."})

        unit = facility.unit

        if unit is not None:
            unit_membership = user.get_unit_membership(unit)

            if unit_membership.has_edit_patient_permission:
                raise ValidationError({'facility': 'Permission denied.'})
