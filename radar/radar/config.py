import string

from flask import current_app
from werkzeug.local import LocalProxy

from radar.utils import random_string


config = LocalProxy(lambda: get_config())


def get_config():
    return current_app.config


class ConfigError(Exception):
    pass


def check_config(config):
    debug = config.setdefault('DEBUG', False)
    testing = config.setdefault('TESTING', False)

    if config.get('SECRET_KEY') is None:
        config['SECRET_KEY'] = random_string(string.ascii_letters + string.digits, 64)

    if config.get('SQLALCHEMY_DATABASE_URI') is None:
        raise ConfigError('Missing SQLALCHEMY_DATABASE_URI')

    config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', False)

    base_url = config.setdefault('BASE_URL', 'http://localhost/#')

    if base_url.endswith('/'):
        raise ConfigError('BASE_URL should not have a trailing slash')

    config.setdefault('READ_ONLY', False)

    config.setdefault('SESSION_TIMEOUT', 1800)  # 30 mins

    config.setdefault('PASSWORD_ALPHABET', string.ascii_lowercase + string.digits)
    config.setdefault('PASSWORD_LENGTH', 10)
    config.setdefault('PASSWORD_RESET_MAX_AGE', 86400)  # 1 day
    config.setdefault('PASSWORD_MIN_SCORE', 3)

    # Password hashing method to use
    # 50000 iterations
    # Note: updating this will cause passwords to be re-hashed when the user next logs in
    config.setdefault('PASSWORD_HASH_METHOD', 'pbkdf2:sha1:50000')

    config.setdefault('EMAIL_ENABLED', not (debug or testing))
    config.setdefault('EMAIL_FROM_ADDRESS', 'RaDaR <radar@radar.nhs.uk>')  # TODO
    config.setdefault('EMAIL_SMTP_HOST', 'localhost')
    config.setdefault('EMAIL_SMTP_PORT', 25)

    config.setdefault('UKRDC_SEARCH_ENABLED', False)

    if config['UKRDC_SEARCH_ENABLED']:
        config.setdefault('UKRDC_SEARCH_TIMEOUT', 10)

        if config.get('UKRDC_SEARCH_URL') is None:
            raise ConfigError('Missing UKRDC_SEARCH_URL')
