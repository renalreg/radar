from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import InputRequired
from wtforms.widgets import TextArea


class StoryForm(Form):
    title = StringField(validators=[InputRequired()])
    body = StringField(validators=[InputRequired()], widget=TextArea())