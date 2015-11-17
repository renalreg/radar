import random
import string

SECRET_KEY = ''.join(random.sample(string.printable, 32))
SQLALCHEMY_DATABASE_URI = 'postgres://radar:{{ db_password }}@{{ db_host }}/radar'
BASE_URL = 'http://localhost/#'
