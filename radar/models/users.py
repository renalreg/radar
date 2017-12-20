from sqlalchemy import Boolean, Column, DateTime, ForeignKey, func, Index, Integer, select, String, text
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import column_property, relationship

from radar.auth.passwords import check_password_hash, generate_password_hash, get_password_hash_method
from radar.database import db
from radar.models.common import CreatedDateMixin, ModifiedDateMixin
from radar.models.logs import Log, log_changes


class UserCreatedUserMixin(object):
    @declared_attr
    def created_user_id(cls):
        # Nullable as it is a self-reference
        return Column(Integer, ForeignKey('users.id'), nullable=True)

    @declared_attr
    def created_user(cls):
        return relationship(
            'User',
            primaryjoin="User.id == %s.created_user_id" % cls.__name__,
            remote_side='User.id', post_update=True)


class UserModifiedUserMixin(object):
    @declared_attr
    def modified_user_id(cls):
        # Nullable as it is a self-reference
        return Column(Integer, ForeignKey('users.id'), nullable=True)

    @declared_attr
    def modified_user(cls):
        return relationship(
            'User',
            primaryjoin="User.id == %s.modified_user_id" % cls.__name__,
            remote_side='User.id', post_update=True)


@log_changes
class User(db.Model, UserCreatedUserMixin, UserModifiedUserMixin, CreatedDateMixin, ModifiedDateMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    _username = Column('username', String, nullable=False)
    _password = Column('password', String)
    _email = Column('email', String)
    first_name = Column(String)
    last_name = Column(String)
    telephone_number = Column(String)
    is_admin = Column(Boolean, default=False, nullable=False, server_default=text('false'))
    is_bot = Column(Boolean, default=False, nullable=False, server_default=text('false'))
    is_enabled = Column(Boolean, default=True, nullable=False, server_default=text('true'))

    reset_password_token = Column(String)
    reset_password_date = Column(DateTime)

    force_password_change = Column(Boolean, default=False, nullable=False, server_default=text('false'))

    last_login_date = column_property(
        select([func.max(Log.date)]).where(Log.user_id == id).where(Log.type == 'LOGIN')
    )

    last_active_date = column_property(
        select([func.max(Log.date)]).where(Log.user_id == id)
    )

    @hybrid_property
    def username(self):
        return self._username

    @username.setter
    def username(self, username):
        if username is not None:
            username = username.lower()

        self._username = username

    @hybrid_property
    def email(self):
        return self._email

    @email.setter
    def email(self, email):
        if email is not None:
            email = email.lower()

        self._email = email

    @property
    def groups(self):
        return [x.group for x in self.group_users]

    def password(self, value):
        self.password_hash = generate_password_hash(value)
        self.reset_password_token = None

    password = property(None, password)

    @property
    def password_hash(self):
        return self._password

    @password_hash.setter
    def password_hash(self, value):
        self._password = value

    def check_password(self, password):
        return (
            self.password_hash is not None and
            check_password_hash(self.password_hash, password)
        )

    @property
    def needs_password_rehash(self):
        new_hash_method = get_password_hash_method()

        if self.password_hash is None:
            r = False
        else:
            current_hash_method = self.password_hash.split('$')[0]
            r = current_hash_method != new_hash_method

        return r

    @property
    def name(self):
        if self.first_name and self.last_name:
            return '{} {}'.format(self.first_name, self.last_name)
        elif self.first_name:
            return self.first_name
        elif self.last_name:
            return self.last_name
        return None

    @classmethod
    def is_authenticated(cls):
        return True


# Ensure usernames are unique
Index('users_username_idx', func.lower(User.username), unique=True)


class AnonymousUser(object):
    @classmethod
    def is_authenticated(cls):
        return False
