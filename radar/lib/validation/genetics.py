from radar.lib.validation.core import run_validators
from radar.lib.validation.validators import required, not_in_future


def validate_genetics(errors, obj):
    run_validators(errors, 'sample_sent', obj.sample_sent, [required, not_in_future])

    if obj.sample_sent is not None:
        run_validators(errors, 'sample_sent_date', obj.sample_sent_date, [required, not_in_future])
