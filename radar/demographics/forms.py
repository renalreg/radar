from flask_wtf import Form
from wtforms import StringField


class DemographicsForm(Form):
    first_name = StringField()
    last_name = StringField()

    def populate_obj(self, obj):
        obj.first_name = self.first_name.data
        obj.last_name = self.last_name.data