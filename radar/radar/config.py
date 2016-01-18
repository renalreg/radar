import string

from flask import current_app

from radar.serializers.core import Serializer
from radar.serializers.fields import StringField, IntegerField, BooleanField, FloatField
from radar.validation.core import Validation, Field, ValidationError, pass_call
from radar.validation.validators import required, min_crack_time, \
    sqlalchemy_connection_string, optional, min_, url, no_trailing_slash, default, \
    max_, min_length, email_address
from radar.utils import random_string

SECRET_KEY_MIN_CRACK_TIME = 1000 * 365 * 24 * 60 * 60  # 1000 years in seconds

DEFAULT_DEBUG = False
DEFAULT_SESSION_TIMEOUT = 1800

DEFAULT_UKRDC_SEARCH_ENABLED = False
DEFAULT_UKRDC_SEARCH_TIMEOUT = 10

# Parameters to use for password generation
# log2(36 ^ 10) = ~51 bits
DEFAULT_PASSWORD_ALPHABET = string.ascii_lowercase + string.digits
DEFAULT_PASSWORD_LENGTH = 10

DEFAULT_PASSWORD_RESET_MAX_AGE = 86400  # 1 day
DEFAULT_PASSWORD_MIN_SCORE = 3

DEFAULT_EMAIL_ENABLED = False
DEFAULT_EMAIL_FROM_ADDRESS = 'RaDaR <radar@radar.nhs.uk>'
DEFAULT_EMAIL_SMTP_HOST = 'localhost'
DEFAULT_EMAIL_SMTP_PORT = 25

DEFAULT_SECRET_KEY = random_string(string.ascii_letters + string.digits, 64)


class InvalidConfig(Exception):
    def __init__(self, path, message):
        self.path = path
        self.message = message

    def __str__(self):
        return 'Invalid config: %s - %s' % (self.path, self.message)


class ConfigSerializer(Serializer):
    DEBUG = BooleanField()
    SECRET_KEY = StringField()
    SQLALCHEMY_DATABASE_URI = StringField()
    SQLALCHEMY_TRACK_MODIFICATIONS = BooleanField()

    BASE_URL = StringField()

    SESSION_TIMEOUT = IntegerField()

    PASSWORD_ALPHABET = StringField()
    PASSWORD_LENGTH = IntegerField()
    PASSWORD_RESET_MAX_AGE = IntegerField()
    PASSWORD_MIN_SCORE = IntegerField()

    EMAIL_ENABLED = BooleanField()
    EMAIL_FROM_ADDRESS = StringField()
    EMAIL_SMTP_HOST = StringField()
    EMAIL_SMTP_PORT = IntegerField()

    UKRDC_SEARCH_ENABLED = BooleanField()
    UKRDC_SEARCH_URL = StringField()
    UKRDC_SEARCH_TIMEOUT = FloatField()


class ConfigValidation(Validation):
    DEBUG = Field([default(DEFAULT_DEBUG)])
    SECRET_KEY = Field([default(DEFAULT_SECRET_KEY), min_crack_time(SECRET_KEY_MIN_CRACK_TIME)])
    SQLALCHEMY_DATABASE_URI = Field([required(), sqlalchemy_connection_string()])
    SQLALCHEMY_TRACK_MODIFICATIONS = Field([default(False)])

    BASE_URL = Field([required(), url(), no_trailing_slash()])

    SESSION_TIMEOUT = Field([default(DEFAULT_SESSION_TIMEOUT), min_(0)])

    PASSWORD_ALPHABET = Field([default(DEFAULT_PASSWORD_ALPHABET), min_length(1)])
    PASSWORD_LENGTH = Field([default(DEFAULT_PASSWORD_LENGTH), min_(1)])
    PASSWORD_RESET_MAX_AGE = Field([default(DEFAULT_PASSWORD_RESET_MAX_AGE), min_(0)])
    PASSWORD_MIN_SCORE = Field([default(DEFAULT_PASSWORD_MIN_SCORE), min_(0), max_(4)])

    EMAIL_ENABLED = Field([optional()])
    EMAIL_FROM_ADDRESS = Field([default(DEFAULT_EMAIL_FROM_ADDRESS), email_address(name=True)])
    EMAIL_SMTP_HOST = Field([default(DEFAULT_EMAIL_SMTP_HOST)])
    EMAIL_SMTP_PORT = Field([default(DEFAULT_EMAIL_SMTP_PORT)])

    UKRDC_SEARCH_ENABLED = Field([default(DEFAULT_UKRDC_SEARCH_ENABLED)])
    UKRDC_SEARCH_URL = Field([optional(), url()])
    UKRDC_SEARCH_TIMEOUT = Field([default(DEFAULT_UKRDC_SEARCH_TIMEOUT), min_(0)])

    @pass_call
    def validate(self, call, obj):
        if obj['UKRDC_SEARCH_ENABLED']:
            # URL is required if UKRDC search is enabled
            call.validators_for_field([required()], obj, self.UKRDC_SEARCH_URL)

        if obj['EMAIL_ENABLED'] is None:
            # Disable emails by default in debug mode
            call.validators_for_field([default(not obj['DEBUG'])], obj, self.EMAIL_ENABLED)

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
        raise InvalidConfig(path, message)

    return new_config


def get_config_value(key):
    return current_app.config[key]
