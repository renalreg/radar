from radar.lib.validation.core import Validation, Field
from radar.lib.validation.meta import MetaValidationMixin
from radar.lib.validation.validators import required


class PostValidation(MetaValidationMixin, Validation):
    title = Field([required()])
    body = Field([required()])
    published_date = Field([required()])
