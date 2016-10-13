from radar.auth.passwords import (
    password_to_nato_str,
    check_password_hash,
    generate_password_hash,
    generate_password,
    get_password_length,
    is_strong_password,
)
from radar.models.users import User


def test_password_to_nato_str():
    password = 'aAzZ123'
    assert password_to_nato_str(password) == 'lower alfa, UPPER ALFA, lower zulu, UPPER ZULU, ONE, TWO, THREE'


def test_password_hash():
    password = 'password123'
    password_hash = generate_password_hash('password123')
    assert password_hash != password
    assert check_password_hash(password_hash, password)


def test_generate_password(app):
    with app.app_context():
        password = generate_password()
        assert len(password) == get_password_length()


def test_weak_passwords(app):
    with app.app_context():
        assert not is_strong_password('password123')
        assert not is_strong_password('rarediseaseregistry418')
        assert not is_strong_password('abcdefghijklmnopqrstuvwyz0123456789')


def test_strong_passwords(app):
    with app.app_context():
        assert is_strong_password('besiderisingwoodennearer')
        assert is_strong_password('7pJnW4yUWx')


def test_weak_passwords_for_user(app):
    user = User()
    user.username = 'dtclihbswm'
    user.email = 'rihylunxov@example.org'
    user.first_name = 'fvgmptirzl'
    user.last_name = 'uehnpqjarf'

    suffix = 'hello418'
    username_password = user.username + suffix
    email_password = user.email + suffix
    first_name_password = user.first_name + suffix
    last_name_password = user.last_name + suffix

    with app.app_context():
        assert is_strong_password(username_password)
        assert not is_strong_password(username_password, user)

        assert is_strong_password(email_password)
        assert not is_strong_password(email_password, user)

        assert is_strong_password(first_name_password)
        assert not is_strong_password(first_name_password, user)

        assert is_strong_password(last_name_password)
        assert not is_strong_password(last_name_password, user)
