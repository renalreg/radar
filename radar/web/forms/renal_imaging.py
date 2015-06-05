from flask_wtf import Form
from wtforms import StringField, DecimalField
from wtforms.validators import InputRequired, Optional
from wtforms.widgets import TextArea

from radar.web.forms.core import RadarDateField, RadarSelectField, RadarYesNoField, RadarInlineRadioField, RadarMeasurementInput, \
    FacilityFormMixin


class RenalImagingForm(FacilityFormMixin, Form):
    date = RadarDateField()

    imaging_type = RadarSelectField(choices=[
        ('', ''),
        ('USS', 'USS'),
        ('CT', 'CT'),
        ('MRI', 'MRI'),
    ], validators=[InputRequired()])

    right_present = RadarYesNoField('Right Kidney', validators=[InputRequired()])
    right_type = RadarInlineRadioField('Kidney Type', choices=[('natural', 'Natural'), ('transplant', 'Transplant')], validators=[Optional()])
    right_length = DecimalField('Renal Length', widget=RadarMeasurementInput('cm'), validators=[Optional()])
    right_cysts = RadarYesNoField('Renal Cysts', validators=[Optional()])
    right_calcification = RadarYesNoField('Calcification Present', validators=[Optional()])
    right_nephrocalcinosis = RadarYesNoField('Nephrocalcinosis', validators=[Optional()])
    right_nephrolithiasis = RadarYesNoField('Nephrolithiasis', validators=[Optional()])
    right_other_malformation = StringField('Other Renal Malformation Details', widget=TextArea(), validators=[Optional()])

    left_present = RadarYesNoField('Left Kidney', validators=[InputRequired()])
    left_type = RadarInlineRadioField('Kidney Type', choices=[('natural', 'Natural'), ('transplant', 'Transplant')], validators=[Optional()])
    left_length = DecimalField('Renal Length', widget=RadarMeasurementInput('cm'), validators=[Optional()])
    left_cysts = RadarYesNoField('Renal Cysts', validators=[Optional()])
    left_calcification = RadarYesNoField('Calcification Present', validators=[Optional()])
    left_nephrocalcinosis = RadarYesNoField('Nephrocalcinosis', validators=[Optional()])
    left_nephrolithiasis = RadarYesNoField('Nephrolithiasis', validators=[Optional()])
    left_other_malformation = StringField('Other Renal Malformation Details', widget=TextArea(), validators=[Optional()])
