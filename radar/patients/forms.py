from radar.form_handlers import FormHandler, str_parser, int_parser, date_parser


class PatientSearchFormHandler(FormHandler):
    parsers = {
        'first_name': str_parser,
        'last_name': str_parser,
        'unit_id': int_parser,
        'disease_group_id': int_parser,
        'date_of_birth': date_parser(),
    }