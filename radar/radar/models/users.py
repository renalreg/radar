from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, func, Index, text

from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from radar.auth.passwords import check_password_hash, generate_password_hash, HASH_METHOD
from radar.database import db
from radar.models.groups import GroupUser
from radar.models.common import ModifiedDateMixin, CreatedDateMixin


class UserCreatedUserMixin(object):
    @declared_attr
    def created_user_id(cls):
        # Nullable as it is a self-reference
        return Column(Integer, ForeignKey('users.id'), nullable=True)

    @declared_attr
    def created_user(cls):
        return relationship('User', primaryjoin="User.id == %s.created_user_id" % cls.__name__, remote_side='User.id', post_update=True)


class UserModifiedUserMixin(object):
    @declared_attr
    def modified_user_id(cls):
        # Nullable as it is a self-reference
        return Column(Integer, ForeignKey('users.id'), nullable=True)

    @declared_attr
    def modified_user(cls):
        return relationship('User', primaryjoin="User.id == %s.modified_user_id" % cls.__name__, remote_side='User.id', post_update=True)


class User(db.Model, UserCreatedUserMixin, UserModifiedUserMixin, CreatedDateMixin, ModifiedDateMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    _username = Column('username', String, nullable=False)
    password_hash = Column(String)
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

    group_users = relationship('GroupUser', back_populates='user', foreign_keys=[GroupUser.user_id])

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        self._password = None

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

    @property
    def password(self):
        return getattr(self, '_password', None)

    @password.setter
    def password(self, value):
        self._password = value
        self.password_hash = generate_password_hash(value)
        self.reset_password_token = None

    def check_password(self, password):
        return (
            self.password_hash is not None and
            check_password_hash(self.password_hash, password)
        )

    @property
    def is_old_password_hash(self):
        if self.password_hash is None:
            r = False
        else:
            hash_method = self.password_hash.split('$')[0]
            r = hash_method != HASH_METHOD
            print r, hash_method, HASH_METHOD

        return r

    @classmethod
    def is_authenticated(cls):
        return True

# Ensure usernames are unique
Index('users_username_idx', func.lower(User.username), unique=True)


class AnonymousUser(object):
    @classmethod
    def is_authenticated(cls):
        return False
