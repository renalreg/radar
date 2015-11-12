from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey

from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from radar.auth.passwords import check_password_hash, generate_password_hash
from radar.database import db
from radar.models import OrganisationUser, CohortUser
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
    _username = Column('username', String, nullable=False, unique=True)
    password_hash = Column(String, nullable=False)
    _email = Column('email', String, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    is_admin = Column(Boolean, default=False, nullable=False)
    is_bot = Column(Boolean, default=False, nullable=False)
    is_enabled = Column(Boolean, default=True, nullable=False)

    reset_password_token = Column(String)
    reset_password_date = Column(DateTime)

    force_password_change = Column(Boolean, default=False, nullable=False)

    organisation_users = relationship('OrganisationUser', back_populates='user', foreign_keys=[OrganisationUser.user_id])
    cohort_users = relationship('CohortUser', back_populates='user', foreign_keys=[CohortUser.user_id])

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
    def organisations(self):
        return [x.organisation for x in self.organisation_users]

    @property
    def cohorts(self):
        return [x.cohort for x in self.cohort_users]

    @property
    def password(self):
        return getattr(self, '_password', None)

    @password.setter
    def password(self, value):
        self._password = value
        self.password_hash = generate_password_hash(value)
        self.reset_password_token = None
        self.force_password_change = False

    def set_initial_password(self, value):
        self._password = value
        self.force_password_change = True

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @classmethod
    def is_authenticated(cls):
        return True


class AnonymousUser(object):
    @classmethod
    def is_authenticated(cls):
        return False
