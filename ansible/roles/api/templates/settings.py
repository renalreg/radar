# {{ ansible_managed }}

SECRET_KEY = open('{{ api_secret_key_path }}', 'rb').read()
SQLALCHEMY_DATABASE_URI = 'postgres://radar:{{ db_password }}@{{ db_host }}/radar'
SESSION_TIMEOUT = 3600
BASE_URL = '{{ web_base_url }}'
UKRDC_PATIENT_SEARCH_URL = 'http://localhost:5100/search'
