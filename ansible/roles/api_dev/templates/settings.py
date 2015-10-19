#{{ ansible_managed }}

DEBUG = True
SECRET_KEY = 'CHANGE_ME'
SQLALCHEMY_DATABASE_URI = 'postgres:///radar'
SESSION_TIMEOUT = 86400
