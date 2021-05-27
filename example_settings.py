SECRET_KEY = 'SECRET'
SQLALCHEMY_DATABASE_URI = 'postgres://radar:password@radar-db/bch'
DEBUG = True

SESSION_TIMEOUT = 3600
BASE_URL = 'http://radar-api:8080'
LIVE = False
READ_ONLY = False

UKRDC_SEARCH_ENABLED = True
UKRDC_SEARCH_URL = 'http://rr-hs-test.northbristol.local:9990/search'
UKRDC_SEARCH_TIMEOUT = 60

UKRDC_EXPORTER_URL = 'http://rr-hs-test.northbristol.local:9990/importandregister'
UKRDC_EXPORTER_STATE = '/tmp/exporter.state'

CELERY_BROKER_URL = 'amqp://guest@localhost//'
CELERY_RESULT_BACKEND = 'rpc://'
CELERY_RESULT_PERSISTENT = False
