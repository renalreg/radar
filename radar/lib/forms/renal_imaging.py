from flask_wtf import Form
from wtforms import StringField, DecimalField
from wtforms.widgets import TextArea

from radar.lib.forms.common import RadarDateField, RadarSelectField, RadarYesNoField, RadarInlineRadioField, RadarMeasurementInput


class RenalImagingForm(Form):
    date = RadarDateField()

    imaging_type = RadarSelectField(choices=[
        ("USS", "USS"),
        ("CT", "CT"),
        ("MRI", "MRI"),
    ])

    right_present = RadarYesNoField("Right Kidney")
    right_type = RadarInlineRadioField("Kidney Type", choices=[("natural", "Natural"), ("transplant", "Transplant")], default="")
    right_length = DecimalField("Renal Length", widget=RadarMeasurementInput("cm"))
    right_cysts = RadarYesNoField("Renal Cysts")
    right_calcification = RadarYesNoField("Calcification Present")
    right_nephrocalcinosis = RadarYesNoField("Nephrocalcinosis")
    right_nephrolithiasis = RadarYesNoField("Nephrolithiasis")
    right_other_malformation = StringField("Other Renal Malformation Details", widget=TextArea())

    left_present = RadarYesNoField("Left Kidney")
    left_type = RadarInlineRadioField("Kidney Type", choices=[("natural", "Natural"), ("transplant", "Transplant")], default="")
    left_length = DecimalField("Renal Length", widget=RadarMeasurementInput("cm"))
    left_cysts = RadarYesNoField("Renal Cysts")
    left_calcification = RadarYesNoField("Calcification Present")
    left_nephrocalcinosis = RadarYesNoField("Nephrocalcinosis")
    left_nephrolithiasis = RadarYesNoField("Nephrolithiasis")
    left_other_malformation = StringField("Other Renal Malformation Details", widget=TextArea())