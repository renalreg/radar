from radar.form_handlers import FormHandler, str_parser, datetime_parser, int_parser
from radar.medications.validators import MedicationValidator


class MedicationFormHandler(FormHandler):
    parsers = {
        'from_date': datetime_parser('%d/%m/%Y'),
        'to_date': datetime_parser('%d/%m/%Y'),
        'name': str_parser,
        'dosage': int_parser,
    }

    def validate(self):
        validator = MedicationValidator(self.obj)

        if not validator.valid():
            self.add_errors(validator.errors)