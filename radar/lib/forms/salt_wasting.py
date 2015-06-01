from flask_wtf import Form
from wtforms import StringField, TextAreaField, IntegerField
from wtforms.validators import InputRequired, NumberRange, Optional
from wtforms.widgets import TextArea

from radar.lib.forms.core import RadarYesNoField


class SaltWastingClinicalFeaturesForm(Form):
    normal_pregnancy = RadarYesNoField("Was mother's pregnancy normal?", validators=[InputRequired()])
    abnormal_pregnancy_text = StringField("If abnormal describe", widget=TextArea())

    neurological_problems = RadarYesNoField("Neurological problems", validators=[InputRequired()])
    seizures = RadarYesNoField()
    abnormal_gait = RadarYesNoField()
    deafness = RadarYesNoField()
    other_neurological_problem = RadarYesNoField("Other")
    other_neurological_problem_text = StringField("Other text", widget=TextArea())

    joint_problems = RadarYesNoField("Joint problems", validators=[InputRequired()])
    joint_problems_age = IntegerField("Age first noticed", validators=[Optional(), NumberRange(min=0, max=120)])
    x_ray_abnormalities = RadarYesNoField("X-ray abnormalities")
    chondrocalcinosis = RadarYesNoField()
    other_x_ray_abnormality = RadarYesNoField("Other X-ray abnormality")
    other_x_ray_abnormality_text = TextAreaField("Other text", widget=TextArea())