from flask_wtf import Form
from wtforms import StringField, SelectField, DateField, IntegerField
from wtforms.validators import Optional

PER_PAGE_CHOICES = [(10, '10'), (25, '25'), (50, '50'), (100, '100'), (-1, 'All')]
PER_PAGE_DEFAULT = 50
ORDER_BY_CHOICES = [
    ('radar_id', 'RaDaR ID'),
    ('first_name', 'First Name'),
    ('last_name', 'Last Name'),
    ('date_of_birth', 'Date of Birth'),
    ('gender', 'Gender'),
]

def optional_int(value):
    if not value:
        return None

    return int(value)

class PatientSearchForm(Form):
    first_name = StringField()
    last_name = StringField()
    unit_id = SelectField('Unit', coerce=optional_int, validators=[Optional()])
    disease_group_id = SelectField('Disease Group', coerce=optional_int, validators=[Optional()])
    date_of_birth = DateField('Date of Birth', format='%d/%m/%Y', validators=[Optional()])
    patient_number = StringField()
    gender = SelectField(choices=[('', ''), ('M', 'Male'), ('F', 'Female')], validators=[Optional()])
    radar_id = IntegerField('RaDaR ID', validators=[Optional()])
    year_of_birth = IntegerField('Year of Birth', validators=[Optional()])
    order_by = SelectField(choices=ORDER_BY_CHOICES)
    order_direction = SelectField(choices=[('asc', 'Ascending'), ('desc', 'Descending')])
    per_page = SelectField(coerce=int, default=50, choices=PER_PAGE_CHOICES)
    page = IntegerField()