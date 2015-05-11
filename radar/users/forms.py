from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import InputRequired, Optional, Email

from radar.forms import RadarSelectField
from radar.users.models import User
from radar.utils import optional_int


class DiseaseGroupRoleForm(Form):
    disease_group_id = RadarSelectField('Disease Group', coerce=int, validators=[InputRequired()])
    role = RadarSelectField(validators=[Optional()])


class UnitRoleForm(Form):
    unit_id = RadarSelectField('Unit', coerce=int, validators=[InputRequired()])
    role = RadarSelectField(validators=[Optional()])


class UserSearchForm(Form):
    username = StringField(validators=[Optional()])
    email = StringField(validators=[Optional()])
    unit_id = RadarSelectField('Unit', coerce=optional_int, validators=[Optional()])
    disease_group_id = RadarSelectField('Disease Group', coerce=optional_int, validators=[Optional()])


class AddUserForm(Form):
    username = StringField(validators=[InputRequired()])
    email = StringField(validators=[InputRequired(), Email()])

    def validate(self):
        if not super(AddUserForm, self).validate():
            return False

        valid = True

        if User.query.filter(User.username == self.username.data).count() > 0:
            self.username.errors.append('Username taken.')
            valid = False

        if User.query.filter(User.email == self.email.data).count() > 0:
            self.email.errors.append('An account already exists with this email address.')
            valid = False

        return valid