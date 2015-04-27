from wtforms import SelectField, Form, StringField


class UserSearchForm(Form):
    username = StringField()
    email = StringField()
    unit_id = SelectField()
    disease_group_id = SelectField()

class UserDiseaseGroupForm(Form):
    disease_group_id = SelectField()

class UserUnitForm(Form):
    unit_id = SelectField()