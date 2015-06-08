from radar.lib.validation.core import ValidationError


def after_date_of_birth(patient):
    def f(value):
        earliest_date_of_birth = patient.earliest_date_of_birth

        if earliest_date_of_birth is not None and value < earliest_date_of_birth:
            raise ValidationError("Value is before the patient's date of birth (%s)." % earliest_date_of_birth.strftime('%d/%m/%Y'))

    return f
