from flask_wtf import Form
from wtforms import DateField, StringField
from wtforms.validators import InputRequired


class MedicationForm(Form):
    from_date = DateField(format='%d/%m/%Y', validators=[InputRequired()])
    to_date = DateField(format='%d/%m/%Y', validators=[InputRequired()])
    name = StringField(validators=[InputRequired()])

    def populate_obj(self, obj):
        obj.from_date = self.from_date.data
        obj.to_date = self.to_date.data
        obj.name = self.name.data