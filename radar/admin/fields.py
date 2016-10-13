from wtforms import SelectFieldBase
from wtforms import widgets


class EnumSelectField(SelectFieldBase):
    """Select field for Enum types."""

    widget = widgets.Select()

    def __init__(self, enum_class, **kwargs):
        super(EnumSelectField, self).__init__(**kwargs)
        self.enum_class = enum_class

    def coerce(self, value):
        """Convert the submitted value to an enum value."""

        if value is not None:
            value = self.enum_class(value)

        return value

    def iter_choices(self):
        """Generate a list of choices."""

        for enum in self.enum_class:
            yield (enum.name, enum.value, enum == self.data)

    def process_formdata(self, valuelist):
        """Handle incoming form data."""

        if valuelist:
            try:
                # Attempt to convert the value (unicode) to an enum value
                self.data = self.coerce(valuelist[0])
            except ValueError:
                raise ValueError(self.gettext('Not a valid choice'))
