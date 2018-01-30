from cornflake.exceptions import ValidationError
import jsonschema

from radar.marmoset.exceptions import SchemaError
from radar.marmoset.utils import wrap

true_f, false_f = wrap(True), wrap(False)
required_f, optional_f = true_f, false_f
visible_f, hidden_f = true_f, false_f


class Schema(object):
    def __init__(self, registry, schema_data):
        try:
            jsonschema.validate(schema_data, registry.schema)
        except jsonschema.SchemaError as e:
            print(e)
            raise SchemaError()

        self.registry = registry
        self.fields = []

        for field_data in schema_data['fields']:
            self.fields.append(Field(self, field_data))

    @property
    def writable_fields(self):
        # Fields that aren't read only
        for field in self.fields:
            if not field.read_only:
                yield field

    @property
    def calculated_fields(self):
        # Fields with a formula
        for field in self.fields:
            if field.formula:
                yield field

    def parse(self, raw_data):
        errors = {}
        data = {}

        # Fields that can be written to
        for field in self.writable_fields:
            name = field.name
            parser = field.parser

            value = raw_data.get(name)

            # Skip null values
            if value is not None:
                try:
                    value = parser(value)
                except ValueError as e:
                    # Gather errors
                    errors[name] = str(e)
                    continue

            data[name] = value

        if errors:
            raise ValidationError(errors)

        return data

    def format(self, data):
        raw_data = {}

        for field in self.fields:
            name = field.name

            if field.formula:
                # Re-calculate the field's value
                value = field.formula(data, [name])
            else:
                value = data.get(name)

            if value is not None:
                value = field.formatter(value)

            raw_data[name] = value

        return raw_data

    def check_default(self, data):
        for field in self.writable_fields:
            name = field.name
            value = data[name]

            if value is None:
                data[name] = field.default(data, [name])

    def check_required(self, data):
        errors = {}

        for field in self.writable_fields:
            name = field.name
            required = field.required
            value = data[name]

            if required(data, [name]) and value is None:
                errors[name] = 'This field is required.'

        if errors:
            raise ValidationError(errors)

    def check_visible(self, data):
        for field in self.writable_fields:
            name = field.name
            visible = field.visible

            # Invisible fields shouldn't have values
            if not visible(data, [name]):
                data[name] = None

    def check_validators(self, data):
        errors = {}

        for field in self.writable_fields:
            name = field.name
            value = data[name]

            if value is None:
                continue

            validators = field.validators

            for validator in validators:
                try:
                    validator(value)
                except ValidationError as e:
                    # Gather errors
                    errors[name] = e.errors
                    break

        if errors:
            raise ValidationError(errors)

    def check_formula(self, data):
        for field in self.calculated_fields:
            name = field.name

            # Calculate the field's value
            data[name] = field.formula(data, [name])

    def validate(self, raw_data):
        data = self.parse(raw_data)
        self.check_default(data)
        self.check_required(data)
        self.check_visible(data)
        self.check_validators(data)
        self.check_formula(data)
        return data


class Field(object):
    def __init__(self, schema, field_data):
        self.schema = schema
        self.name = field_data['name']
        self.type = field_data['type']
        self.parser = self.registry.get_parser(self.type)
        self.formatter = self.registry.get_formatter(self.type)
        self.validators = []

        # Default to None
        default_data = field_data.get('default')
        self.default = self.parse_default(default_data)

        # Field is read only if it has a formula
        self.read_only = bool(field_data.get('formula'))

        # Required by default
        # Required fields will return an error if the value is None
        # Setting required has no effect on fields with a default
        # Read only fields (e.g. formula) are never required

        if self.read_only:
            required_data = False
        else:
            required_data = field_data.get('required', True)

        self.required = self.parse_required(required_data)

        # Visible by default
        # Hidden fields are set to None during validation
        visible_data = field_data.get('visible', True)
        self.visible = self.parse_visible(visible_data)

        options_data = field_data.get('options')

        if options_data:
            self.validators.append(self.parse_options(options_data))

        validators_data = field_data.get('validators', [])
        self.validators.extend(self.parse_validators(validators_data))

        formula_data = field_data.get('formula')

        if formula_data is None:
            self.formula = None
        else:
            self.formula = self.parse_formula(formula_data)

    def parse_default(self, default_data):
        """Returns a function to get the default value for a field.

        Can be any of:
        * constant (e.g. None, 3, "hello")
        * object - function

        A function allows you to choose a default value based on other
        submitted values or to default to today's date.

        The returned function should have two parameters:

        * form - parsed field values.
        * path - path to the current field as a list.

        The returned function should return a value to use as the default.
        """

        if default_data is None:
            # Default to None
            return wrap(None)
        elif isinstance(default_data, dict):
            # Run a function to get the default value
            name = default_data.get('name')

            if name is None:
                raise SchemaError()

            default = self.registry.get_default(self.type, name)(self, default_data)

            return default
        else:
            # Default to a constant
            try:
                # Need to parse the constant (e.g. dates)
                return wrap(self.parser(default_data))
            except ValueError:
                raise SchemaError()

    def parse_required(self, required_data):
        """Returns a function to determine if a field is required.

        Can be any of:
        * True - field is required
        * False - field is optional
        * object - custom function

        The function option is useful when a field is only required in
        certain situations (e.g. if another field is a particular value).

        The returned function should have two parameters:

        * form - parsed field values.
        * path - path to the current field as a list.

        Note: The path is currently just the name of the field.

        The returned function should return true if the field
        is required.

        Missing values are replaced with nulls when the field is parsed.
        An error is returned if a null value is given for a required field.
        """

        if required_data is True:
            # Field is required (reject None)
            return required_f
        elif required_data is False:
            # Field is optional (accept None)
            return optional_f
        elif isinstance(required_data, dict):
            # Run a function to determine if this field is required
            name = required_data['name']
            required = self.registry.get_required(name)(self, required_data)
            return required
        else:
            # Should never reach here
            raise SchemaError()

    def parse_visible(self, visible_data):
        """Returns a function that determines if the field is visible.

        Fields that are hidden have their value set to None.

        Can be any of:
        * True - field is visible
        * False - field is hidden
        * object - custom function

        The function option can be used to show or hide a field based on
        the value of another field.

        The returned function should have two parameters:

        * form - parsed field values.
        * path - path to the current field as a list.

        Note: The path is currently just the name of the field.

        The returned function should return true if the field
        is visible.
        """

        if visible_data is True:
            # Field is visible
            return visible_f
        elif visible_data is False:
            # Field is hidden (set value to None)
            return hidden_f
        elif isinstance(visible_data, dict):
            # Run a function to determine if this field is visible
            name = visible_data['name']
            visible = self.registry.get_visible(name)(self, visible_data)
            return visible
        else:
            # Should never reach here
            raise SchemaError()

    def parse_options(self, options_data):
        """Converts a list of options to a validator."""

        # TODO validate options

        return self.parse_validator({
            'name': 'in',
            'values': [x['value'] for x in options_data],
        })

    def parse_validator(self, validator_data):
        """Returns a function that checks the value of a field.

        Accepts a dict parameter with a type property to lookup against
        the list of validators.

        The returned function should have three parameters:

        * form - parsed field values.
        * path - path to the current field as a list.
        * value - parsed value of the current field.
        """

        name = validator_data['name']
        validator = self.registry.get_validator(self.type, name)(self, validator_data)
        return validator

    def parse_validators(self, validators_data):
        """Parse a list of validators."""

        if not isinstance(validators_data, list):
            raise SchemaError()

        validators = []

        for validator_data in validators_data:
            validators.append(self.parse_validator(validator_data))

        return validators

    def parse_formula(self, formula_data):
        name = formula_data['name']
        formula = self.registry.get_formula(name)(self, formula_data)
        return formula

    @property
    def registry(self):
        return self.schema.registry
