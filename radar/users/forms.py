from radar.form_handlers import FormHandler, str_parser, int_parser


class UserSearchFormHandler(FormHandler):
    parsers = {
        'username': str_parser,
        'email': str_parser,
        'unit_id': int_parser,
        'disease_group_id': int_parser,
    }