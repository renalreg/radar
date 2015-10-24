from radar.serializers.core import Serializer
from radar.serializers.fields import StringField, IntegerField
from radar.validation.core import Validation, Field, ValidationError
from radar.validation.validators import required, min_crack_time, \
    sqlalchemy_connection_string, optional, min_, url, no_trailing_slash


SECRET_KEY_MIN_CRACK_TIME = 1000 * 365 * 24 * 60 * 60  # 1000 years in seconds


class InvalidConfig(Exception):
    pass


class ConfigSerializer(Serializer):
    SECRET_KEY = StringField()
    SQLALCHEMY_DATABASE_URI = StringField()
    SESSION_TIMEOUT = IntegerField()
    BASE_URL = StringField()


class ConfigValidation(Validation):
    SECRET_KEY = Field([required(), min_crack_time(SECRET_KEY_MIN_CRACK_TIME)])
    SQLALCHEMY_DATABASE_URI = Field([required(), sqlalchemy_connection_string()])
    SESSION_TIMEOUT = Field([optional(), min_(0)])
    BASE_URL = Field([required(), url(), no_trailing_slash()])


def check_config(config):
    serializer = ConfigSerializer()
    validation = ConfigValidation()

    try:
        config = serializer.to_value(config)
        validation.after_update({}, {}, config)
    except ValidationError as e:
        first_error = e.first()
        path = '.'.join(first_error[0])
        message = first_error[1]
        raise InvalidConfig('config error: %s - %s' % (path, message))
