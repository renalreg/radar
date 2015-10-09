from radar.validation.core import Validation, Field
from radar.validation.meta import MetaValidationMixin
from radar.validation.validators import required


class PostValidation(MetaValidationMixin, Validation):
    title = Field([required()])
    body = Field([required()])
    published_date = Field([required()])
