from collections import OrderedDict
import copy

import six


class Result(object):
    def __init__(self):
        self.skipped = False


class ValidationError(Exception):
    def __init__(self, errors):
        self.errors = ValidationError.normalise(errors)

    @staticmethod
    def normalise(errors):
        if isinstance(errors, dict):
            new_errors = OrderedDict()

            for k, v in errors.items():
                if isinstance(v, dict) or isinstance(v, list):
                    v = ValidationError.normalise(v)
                else:
                    v = [v]

                new_errors[k] = v
        elif isinstance(errors, list):
            new_errors = []

            for x in errors:
                if isinstance(x, dict) or isinstance(x, list):
                    x = ValidationError.normalise(x)

                new_errors.append(x)
        else:
            new_errors = [errors]

        return new_errors

    @staticmethod
    def _first(errors):
        r = None

        if isinstance(errors, list):
            for x in errors:
                r = ValidationError._first(x)

                if r is not None:
                    break
        elif isinstance(errors, dict):
            for k, v in errors.items():
                r = ValidationError._first(v)

                if r is not None:
                    if r[0] is None:
                        path = (k,)
                    else:
                        path = (k,) + r[0]

                    r = (path, r[1])
                    break
        else:
            r = (None, errors)

        return r

    def first(self):
        return ValidationError._first(self.errors)

    def __str__(self):
        return str(self.errors)


class SkipField(Exception):
    pass


def pass_context(f):
    f._pass_context = True
    return f


def pass_call(f):
    f._pass_call = True
    return f


def pass_old_obj(f):
    f._pass_old_obj = True
    return f


def pass_new_obj(f):
    f._pass_new_obj = True
    return f


def pass_old_value(f):
    f._pass_old_value = True
    return f


def pass_new_value(f):
    f._pass_new_value = True
    return f


def pass_full(f):
    f._pass_context = True
    f._pass_call = True
    f._pass_old_obj = True
    f._pass_new_obj = True
    f._pass_old_value = True
    f._pass_new_value = True
    return f


class ContextBeforeUpdateCall(object):
    def __init__(self, old_obj):
        self.old_obj = old_obj

    def __call__(self, f, ctx):
        args = [ctx]

        if getattr(f, '_pass_call', False):
            args.append(self)

        if getattr(f, '_pass_old_obj', False):
            args.append(self.old_obj)

        return f(*args)


class ContextCall(object):
    def __init__(self, obj_obj, new_obj):
        self.obj_obj = obj_obj
        self.new_obj = new_obj

    def __call__(self, f, ctx):
        args = [ctx]

        if getattr(f, '_pass_call', False):
            args.append(self)

        if getattr(f, '_pass_old_obj', False):
            args.append(self.obj_obj)

        if getattr(f, '_pass_new_obj', False):
            args.append(self.new_obj)

        return f(*args)


class ValidatorCall(object):
    def __init__(self, ctx, old_value):
        self.ctx = ctx
        self.old_value = old_value

    def __call__(self, f, new_value):
        args = []

        if getattr(f, '_pass_context', False):
            args.append(self.ctx)

        if getattr(f, '_pass_call', False):
            args.append(self)

        if getattr(f, '_pass_old_value', False):
            args.append(self.old_value)

        args.append(new_value)

        return f(*args)

    def validators(self, validators, new_value, result=None):
        return run_validators(validators, self, new_value, result)


class PreValidateCall(object):
    def __init__(self, ctx, old_obj):
        self.ctx = ctx
        self.old_obj = old_obj

    def __call__(self, f, new_obj):
        args = []

        if getattr(f, '_pass_context', False):
            args.append(self.ctx)

        if getattr(f, '_pass_call', False):
            args.append(self)

        if getattr(f, '_pass_old_obj', False):
            args.append(self.old_obj)

        args.append(new_obj)

        return f(*args)


class ValidateBeforeUpdateCall(object):
    def __init__(self, ctx, old_obj):
        self.ctx = ctx
        self.old_obj = old_obj

    def __call__(self, f):
        args = []

        if getattr(f, '_pass_context', False):
            args.append(self.ctx)

        if getattr(f, '_pass_call', False):
            args.append(self)

        args.append(self.old_obj)

        f(*args)


class ValidateCall(object):
    def __init__(self, ctx, old_obj):
        self.ctx = ctx
        self.old_obj = old_obj

    def __call__(self, f, new_obj):
        args = []

        if getattr(f, '_pass_context', False):
            args.append(self.ctx)

        if getattr(f, '_pass_call', False):
            args.append(self)

        if getattr(f, '_pass_old_obj', False):
            args.append(self.old_obj)

        args.append(new_obj)

        return f(*args)

    def validators(self, validators, obj, result=None):
        call = ValidatorCall(self.ctx, self.old_obj)
        return run_validators(validators, call, obj, result)

    def validators_for_field(self, validators, obj, field, result=None):
        old_value = field.get_value(self.old_obj)
        new_value = field.get_value(obj)
        call = ValidatorCall(self.ctx, old_value)

        try:
            new_value = run_validators(validators, call, new_value, result)
        except ValidationError as e:
            raise ValidationError({field.field_name: e.errors})

        field.set_value(obj, new_value)
        return new_value


class ValidateFieldBeforeUpdateCall(object):
    def __init__(self, ctx, old_obj, old_value):
        self.ctx = ctx
        self.old_obj = old_obj
        self.old_value = old_value

    def __call__(self, f):
        args = []

        if getattr(f, '_pass_context', False):
            args.append(self.ctx)

        if getattr(f, '_pass_call', False):
            args.append(self)

        if getattr(f, '_pass_old_obj', False):
            args.append(self.old_obj)

        args.append(self.old_value)

        f(*args)


class ValidateFieldCall(object):
    def __init__(self, ctx, old_obj, new_obj, old_value):
        self.ctx = ctx
        self.old_obj = old_obj
        self.new_obj = new_obj
        self.old_value = old_value

    def __call__(self, f, new_value):
        args = []

        if getattr(f, '_pass_context', False):
            args.append(self.ctx)

        if getattr(f, '_pass_call', False):
            args.append(self)

        if getattr(f, '_pass_old_obj', False):
            args.append(self.old_obj)

        if getattr(f, '_pass_new_obj', False):
            args.append(self.new_obj)

        if getattr(f, '_pass_old_value', False):
            args.append(self.old_value)

        args.append(new_value)

        return f(*args)

    def validators(self, validators, new_value, result=None):
        call = ValidatorCall(self.ctx, self.old_value)
        return run_validators(validators, call, new_value, result)


def run_validators(validators, call, new_value, result=None):
    for validator in validators:
        try:
            new_value = call(validator, new_value)
        except SkipField:
            if result is not None:
                result.skipped = True

            break

    return new_value


class CleanObject(object):
    def __init__(self, data):
        for key, value in data.items():
            setattr(self, key, value)

    def __getitem__(self, key):
        return getattr(self, key)


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
        if isinstance(obj, dict):
            obj[self.field_name] = value
        else:
            setattr(obj, self.field_name, value)

    def get_value(self, obj):
        if obj is None:
            return None
        elif isinstance(obj, dict):
            return obj.get(self.field_name)
        else:
            return getattr(obj, self.field_name)

    def get_validators(self):
        return self.chain

    def get_context_before_update(self, *args):
        return args[0]

    def get_context(self, *args):
        return args[0]

    def validate_before_update(self, *args):
        return args[0]

    def pre_validate(self, *args):
        return args[0]

    def validate(self, *args):
        return args[0]

    def clone(self, obj):
        return obj

    def before_update(self, ctx, old_obj):
        ctx = copy.copy(ctx)

        context_before_update_call = ContextBeforeUpdateCall(old_obj)
        ctx = context_before_update_call(self.get_context_before_update, ctx)

        validate_before_update_call = ValidateBeforeUpdateCall(ctx, old_obj)
        validate_before_update_call(self.validate_before_update)

    def after_update(self, ctx, old_obj, new_obj, result=None):
        ctx = copy.copy(ctx)

        context_call = ContextCall(old_obj, new_obj)
        ctx = context_call(self.get_context, ctx)

        pre_validate_call = PreValidateCall(ctx, old_obj)
        new_obj = pre_validate_call(self.pre_validate, new_obj)

        validator_call = ValidatorCall(ctx, old_obj)
        new_obj = validator_call.validators(self.get_validators(), new_obj, result)

        validate_call = ValidateCall(ctx, old_obj)
        new_obj = validate_call(self.validate, new_obj)

        return new_obj


class ValidationMetaclass(type):
    def __new__(cls, name, bases, attrs):
        fields = ValidationMetaclass.get_fields(bases, attrs)
        attrs['_declared_fields'] = fields
        return super(ValidationMetaclass, cls).__new__(cls, name, bases, attrs)

    @staticmethod
    def sort_fields(fields):
        fields = ValidationMetaclass.unique_fields(fields)
        fields = reversed(fields)
        fields = OrderedDict(fields)
        return fields

    @staticmethod
    def unique_fields(fields):
        new_fields = []
        field_names = set()

        for field_name, field in fields:
            if field_name in field_names:
                continue

            field_names.add(field_name)
            new_fields.append((field_name, field))

        return new_fields

    @staticmethod
    def reverse_sort_by_declaration(fields):
        return sorted(fields, key=lambda x: x[1]._creation_counter, reverse=True)

    @staticmethod
    def get_fields(bases, attrs):
        fields = []

        # Get the fields declared on this class
        for field_name, obj in list(attrs.items()):
            if isinstance(obj, Field):
                fields.append((field_name, attrs.pop(field_name)))

        # Sort the fields in reverse declaration order
        fields = ValidationMetaclass.reverse_sort_by_declaration(fields)

        # Loop through parent classes
        for validation_class in bases:
            if hasattr(validation_class, '_declared_fields'):
                # Copy fields from another validation class
                base_fields = validation_class._declared_fields.items()
            else:
                # Copy fields from mixins
                base_fields = ValidationMetaclass.get_mixin_fields(validation_class).items()

            # Fields on this class and earlier base classes will take precedence
            fields.extend(reversed(base_fields))

        fields = ValidationMetaclass.sort_fields(fields)

        return fields

    @staticmethod
    def get_mixin_fields(validation_class):
        fields = []

        for field_name, obj in validation_class.__dict__.items():
            if isinstance(obj, Field):
                fields.append((field_name, obj))

        # Sort the fields in reverse declaration order
        fields = ValidationMetaclass.reverse_sort_by_declaration(fields)

        for validation_mixin_klass in validation_class.__bases__:
            base_fields = ValidationMetaclass.get_mixin_fields(validation_mixin_klass).items()
            fields.extend(reversed(base_fields))

        fields = ValidationMetaclass.sort_fields(fields)

        return fields


def get_old_value(old_obj, field_name):
    if old_obj is None:
        old_value = None
    elif isinstance(old_obj, dict):
        old_value = old_obj.get(field_name)
    else:
        old_value = getattr(old_obj, field_name)

    return old_value


@six.add_metaclass(ValidationMetaclass)
class Validation(Field):
    def __init__(self, *args, **kwargs):
        super(Validation, self).__init__(*args, **kwargs)
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
            setattr(self, field_name, field)

        return fields

    def clone(self, obj):
        data = {}

        for field_name, field in self.fields.items():
            value = field.get_value(obj)
            data[field_name] = field.clone(value)

        return CleanObject(data)

    def before_update(self, ctx, old_obj):
        ctx = copy.copy(ctx)

        get_context_before_update_call = ContextBeforeUpdateCall(old_obj)
        ctx = get_context_before_update_call(self.get_context_before_update, ctx)

        errors = {}

        for field_name, field in self.fields.items():
            old_value = field.get_value(old_obj)

            try:
                field.before_update(ctx, old_value)

                validate_method = getattr(self, 'validate_before_update_' + field.field_name, None)

                if validate_method is not None:
                    validate_field_before_update_call = ValidateFieldBeforeUpdateCall(ctx, old_obj, old_value)
                    validate_field_before_update_call(validate_method)
            except ValidationError as e:
                errors[field.field_name] = e.errors

        if errors:
            raise ValidationError(errors)

        validate_before_update_call = ValidateBeforeUpdateCall(ctx, old_obj)
        validate_before_update_call(self.validate_before_update)

    def after_update(self, ctx, old_obj, new_obj, result=None):
        if result is None:
            result = Result()

        errors = {}

        context_call = ContextCall(old_obj, new_obj)
        ctx = context_call(self.get_context, ctx)

        pre_validate_call = PreValidateCall(ctx, old_obj)
        new_obj = pre_validate_call(self.pre_validate, new_obj)

        try:
            validator_call = ValidatorCall(ctx, old_obj)
            new_obj = validator_call.validators(self.get_validators(), new_obj, result)
        except ValidationError as e:
            raise ValidationError({'_': e.errors})

        if result.skipped:
            return new_obj

        skipped_fields = set()

        for field_name, field in self.fields.items():
            old_value = get_old_value(old_obj, field_name)
            new_value = field.get_value(new_obj)

            try:
                result = Result()
                new_value = field.after_update(ctx, old_value, new_value, result=result)
                field.set_value(new_obj, new_value)

                if result.skipped:
                    skipped_fields.add(field_name)
            except ValidationError as e:
                errors[field.field_name] = e.errors

        if errors:
            raise ValidationError(errors)

        for field_name, field in self.fields.items():
            if field_name in skipped_fields:
                continue

            old_value = get_old_value(old_obj, field_name)
            new_value = field.get_value(new_obj)

            try:
                validate_method = getattr(self, 'validate_' + field.field_name, None)

                if validate_method is not None:
                    validate_field_call = ValidateFieldCall(ctx, old_obj, new_obj, old_value)
                    new_value = validate_field_call(validate_method, new_value)

                field.set_value(new_obj, new_value)
            except ValidationError as e:
                errors[field.field_name] = e.errors

        if errors:
            raise ValidationError(errors)

        try:
            validate_call = ValidateCall(ctx, old_obj)
            new_obj = validate_call(self.validate, new_obj)
        except ValidationError as e:
            if isinstance(e.errors, dict):
                raise
            else:
                raise ValidationError({'_': e.errors})

        except SkipField:
            if result is not None:
                result.skipped = True

            return new_obj

        return new_obj


class ListField(Field):
    def __init__(self, validation, chain=None):
        super(ListField, self).__init__(chain)
        self.validation = validation

    def before_update(self, ctx, old_obj):
        ctx = copy.copy(ctx)

        context_before_update_call = ContextBeforeUpdateCall(old_obj)
        ctx = context_before_update_call(self.get_context_before_update, ctx)

        if old_obj is not None:
            errors = {}

            for i, old_value in enumerate(old_obj):
                try:
                    self.validation.before_update(ctx, old_value)
                except ValidationError as e:
                    errors[i] = e.errors

            if errors:
                raise ValidationError(errors)

        validate_before_update_call = ValidateBeforeUpdateCall(ctx, old_obj)
        validate_before_update_call(self.validate_before_update)

    def after_update(self, ctx, old_obj, new_obj, result=None):
        ctx = copy.copy(ctx)

        context_call = ContextCall(old_obj, new_obj)
        ctx = context_call(self.get_context, ctx)

        pre_validate_call = PreValidateCall(ctx, old_obj)
        new_obj = pre_validate_call(self.pre_validate, new_obj)

        errors = {}

        try:
            validator_call = ValidatorCall(ctx, old_obj)
            new_obj = validator_call.validators(self.get_validators(), new_obj, result)
        except ValidationError as e:
            raise ValidationError({'_': e.errors})

        new_values = list(new_obj)
        new_obj = []

        for i, new_value in enumerate(new_values):
            if old_obj is None:
                old_value = None
            else:
                try:
                    old_value = old_obj[i]
                except IndexError:
                    old_value = None

            try:
                new_value = self.validation.after_update(ctx, old_value, new_value)
            except ValidationError as e:
                errors[i] = e.errors

            new_obj.append(new_value)

        if errors:
            raise ValidationError(errors)

        validate_call = ValidateCall(ctx, old_obj)
        new_obj = validate_call(self.validate, new_obj)

        return new_obj
