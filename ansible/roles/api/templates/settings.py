# {{ ansible_managed }}

SECRET_KEY = open('{{ api_secret_key_path }}', 'rb').read()
SQLALCHEMY_DATABASE_URI = 'postgres:///radar'
SESSION_TIMEOUT = 3600
