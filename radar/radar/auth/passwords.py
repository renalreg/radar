from random import SystemRandom

import werkzeug.security
import zxcvbn

from radar.config import get_config_value

NATO_ALPHABET = {
    'a': 'ALFA',
    'b': 'BRAVO',
    'c': 'CHARLIE',
    'd': 'DELTA',
    'e': 'ECHO',
    'f': 'FOXTROT',
    'g': 'GOLF',
    'h': 'HOTEL',
    'i': 'INDIA',
    'j': 'JULIETT',
    'k': 'KILO',
    'l': 'LIMA',
    'm': 'MIKE',
    'n': 'NOVEMBER',
    'o': 'OSCAR',
    'p': 'PAPA',
    'q': 'QUEBEC',
    'r': 'ROMEO',
    's': 'SIERRA',
    't': 'TANGO',
    'u': 'UNIFORM',
    'v': 'VICTOR',
    'w': 'WHISKEY',
    'x': 'XRAY',
    'y': 'YANKEE',
    'z': 'ZULU',
    '0': 'ZERO',
    '1': 'ONE',
    '2': 'TWO',
    '3': 'THREE',
    '4': 'FOUR',
    '5': 'FIVE',
    '6': 'SIX',
    '7': 'SEVEN',
    '8': 'EIGHT',
    '9': 'NINE',
}

USER_INPUTS = [
    'disease'
    'group',
    'nhs',
    'radar',
    'rare',
    'renal',
    'registry',
    'study',
    'ukrr'
]


def get_password_alphabet():
    return get_config_value('PASSWORD_ALPHABET')


def get_password_length():
    return get_config_value('PASSWORD_LENGTH')


def get_password_min_score():
    return get_config_value('PASSWORD_MIN_SCORE')


def generate_password():
    alphabet = get_password_alphabet()
    length = get_password_length()
    return ''.join(SystemRandom().sample(alphabet, length))


def generate_password_hash(password):
    # 50000 iterations
    return werkzeug.security.generate_password_hash(password, 'pbkdf2:sha1:50000')


def check_password_hash(password_hash, password):
    return werkzeug.security.check_password_hash(password_hash, password)


def password_to_nato_values(password):
    nato_values = []

    for x in password:
        nato_value = NATO_ALPHABET.get(x.lower(), x)

        if x.isupper():
            nato_value = 'UPPER ' + nato_value
        elif x.islower():
            nato_value = 'lower ' + nato_value.lower()

        nato_values.append(nato_value)

    return nato_values


def password_to_nato_str(password):
    return ', '.join(password_to_nato_values(password))


def password_score(password, user_inputs=None):
    return zxcvbn.password_strength(password, user_inputs)['score']


def is_strong_password(password, user=None):
    min_score = get_password_min_score()

    if user is None:
        user_inputs = USER_INPUTS
    else:
        user_inputs = [
            user.username,
            user.email,
            user.first_name,
            user.last_name
        ]

        # Remove nulls
        user_inputs = [x for x in user_inputs if x]

        user_inputs.extend(USER_INPUTS)

    return password_score(password, user_inputs) >= min_score
