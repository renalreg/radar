from wtforms import SelectFieldBase
from wtforms import widgets


class EnumSelectField(SelectFieldBase):
    widget = widgets.Select()

    def __init__(self, enum_class, **kwargs):
        super(EnumSelectField, self).__init__(**kwargs)
        self.enum_class = enum_class

    def coerce(self, value):
        if value is not None:
            value = self.enum_class(value)

        return value

    def iter_choices(self):
        for enum in self.enum_class:
            yield (enum.name, enum.value, enum == self.data)

    def process_formdata(self, valuelist):
        if valuelist:
            try:
                self.data = self.coerce(valuelist[0])
            except ValueError:
                raise ValueError(self.gettext('Not a valid choice'))
