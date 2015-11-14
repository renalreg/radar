from radar.validation.core import Validation, Field
from radar.validation.meta import MetaValidationMixin
from radar.validation.validators import sanitize_html, not_empty, default_now


class PostValidation(MetaValidationMixin, Validation):
    title = Field([not_empty()])
    published_date = Field([default_now()])
    body = Field([not_empty(), sanitize_html()])
