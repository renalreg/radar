from radar.form_handlers import FormHandler, str_parser


class DemographicsFormHandler(FormHandler):
    parsers = {
        'first_name': str_parser,
        'last_name': str_parser
    }