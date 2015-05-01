from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Optional
from radar.forms import RadarSelectField
from radar.utils import optional_int


class LoginForm(Form):
    username = StringField(validators=[InputRequired()])
    password = PasswordField(validators=[InputRequired()])


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