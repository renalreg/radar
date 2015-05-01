from flask_wtf import Form
from wtforms import SelectField, StringField, PasswordField
from wtforms.validators import InputRequired
from radar.utils import optional_int


class LoginForm(Form):
    username = StringField(validators=[InputRequired()])
    password = PasswordField(validators=[InputRequired()])

class UserDiseaseGroupForm(Form):
    disease_group_id = SelectField(coere=int)
    role = SelectField()

class UserSearchForm(Form):
    username = StringField()
    email = StringField()
    unit_id = SelectField("Disease Group", coerce=optional_int)
    disease_group_id = SelectField("Unit", coerce=optional_int)