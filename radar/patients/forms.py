from radar.form_handlers import FormHandler, str_parser, int_parser, date_parser, positive_int_parser


class PatientSearchFormHandler(FormHandler):
    parsers = {
        'first_name': str_parser,
        'last_name': str_parser,
        'unit_id': int_parser,
        'disease_group_id': int_parser,
        'date_of_birth': date_parser(),
        'patient_number': str_parser,
        'gender': str_parser,
        'radar_id': int_parser,
        'year_of_birth': int_parser,
        'order_by': str_parser,
        'order_direction': str_parser,
        'per_page': int_parser,
        'page': positive_int_parser
    }