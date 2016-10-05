from sqlalchemy.types import Enum, String
from sqlalchemy.types import TypeDecorator, SchemaType


class EnumType(TypeDecorator, SchemaType):
    impl = Enum

    def __init__(self, enum_class, **options):
        enumerants = [x.value for x in enum_class]
        super(EnumType, self).__init__(*enumerants, **options)
        self.enum_class = enum_class

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = value.value

        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = self.enum_class(value)

        return value

    def _set_parent(self, column):
        self.impl._set_parent(column)

    @property
    def python_type(self):
        return self.enum_class


class EnumToStringType(TypeDecorator):
    impl = String

    def __init__(self, enum_class, **options):
        super(EnumToStringType, self).__init__(**options)
        self.enum_class = enum_class

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = value.value

        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = self.enum_class(value)

        return value

    @property
    def python_type(self):
        return self.enum_class
