import base64
import os
from random import SystemRandom
import string

RESET_PASSWORD_MAX_AGE = 86400  # 1 day

# Parameters to user for password generation
GENERATE_PASSWORD_ALPHABET = string.ascii_letters + string.digits
GENERATE_PASSWORD_LENGTH = 10


def generate_reset_password_token():
    return base64.urlsafe_b64encode(os.urandom(32))


def generate_password():
    return ''.join(SystemRandom().sample(GENERATE_PASSWORD_ALPHABET, GENERATE_PASSWORD_LENGTH))
