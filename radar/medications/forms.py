from flask_wtf import Form
from wtforms import DateField, StringField


class MedicationForm(Form):
    from_date = DateField(format='%d/%m/%Y')
    to_date = DateField(format='%d/%m/%Y')
    name = StringField()

    def populate_obj(self, obj):
        obj.from_date = self.from_date.data
        obj.to_date = self.to_date.data
        obj.name = self.name.data