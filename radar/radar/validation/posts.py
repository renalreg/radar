from radar.validation.core import Validation, Field
from radar.validation.meta import MetaValidationMixin
from radar.validation.validators import required, sanitize_html


class PostValidation(MetaValidationMixin, Validation):
    title = Field([required()])
    published_date = Field([required()])
    body = Field([required(), sanitize_html()])
