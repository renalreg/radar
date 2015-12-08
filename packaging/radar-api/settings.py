import random
import string

SECRET_KEY = ''.join(random.sample(string.printable, 32))
SQLALCHEMY_DATABASE_URI = 'postgres://radar@localhost/radar'
BASE_URL = 'http://localhost/#'
