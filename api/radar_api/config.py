from radar.serializers.core import Serializer
from radar.serializers.fields import StringField, IntegerField, BooleanField
from radar.validation.core import Validation, Field, ValidationError, pass_call
from radar.validation.validators import required, min_crack_time, \
    sqlalchemy_connection_string, optional, min_, url, no_trailing_slash, default

SECRET_KEY_MIN_CRACK_TIME = 1000 * 365 * 24 * 60 * 60  # 1000 years in seconds
DEFAULT_SESSION_TIMEOUT = 1800
DEFAULT_UKRDC_SEARCH_ENABLED = False
DEFAULT_UKRDC_SEARCH_TIMEOUT = 10


class InvalidConfig(Exception):
    pass


class ConfigSerializer(Serializer):
    SECRET_KEY = StringField()
    SQLALCHEMY_DATABASE_URI = StringField()
    SESSION_TIMEOUT = IntegerField()
    BASE_URL = StringField()
    UKRDC_SEARCH_ENABLED = BooleanField()
    UKRDC_SEARCH_URL = StringField()


class ConfigValidation(Validation):
    SECRET_KEY = Field([required(), min_crack_time(SECRET_KEY_MIN_CRACK_TIME)])
    SQLALCHEMY_DATABASE_URI = Field([required(), sqlalchemy_connection_string()])
    SESSION_TIMEOUT = Field([default(DEFAULT_SESSION_TIMEOUT), min_(0)])
    BASE_URL = Field([required(), url(), no_trailing_slash()])
    UKRDC_SEARCH_ENABLED = Field([default(DEFAULT_UKRDC_SEARCH_ENABLED)])
    UKRDC_SEARCH_URL = Field([optional(), url()])
    UKRDC_SEARCH_TIMEOUT = Field([default(DEFAULT_UKRDC_SEARCH_TIMEOUT), min_(0)])

    @pass_call
    def validate(self, call, obj):
        if obj['UKRDC_SEARCH_ENABLED']:
            # URL is required if UKRDC search is enabled
            call.validators_for_field([required()], obj, self.UKRDC_SEARCH_URL)

        return obj


def check_config(config):
    serializer = ConfigSerializer()
    validation = ConfigValidation()

    try:
        config = serializer.to_value(config)
        new_config = validation.after_update({}, {}, config)
    except ValidationError as e:
        first_error = e.first()
        path = '.'.join(first_error[0])
        message = first_error[1]
        raise InvalidConfig('config error: %s - %s' % (path, message))

    return new_config
