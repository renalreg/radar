from radar.form_handlers import FormHandler, str_parser, int_parser, date_parser
from radar.medications.validators import MedicationValidator


class MedicationFormHandler(FormHandler):
    parsers = {
        'from_date': date_parser(),
        'to_date': date_parser(),
        'name': str_parser,
        'dosage': int_parser,
    }

    def validate(self):
        validator = MedicationValidator(self.obj)

        if not validator.valid():
            self.add_errors(validator.errors)