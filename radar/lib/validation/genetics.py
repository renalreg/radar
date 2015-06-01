from radar.lib.validation.core import run_validators, required


def validate_genetics(errors, obj):
    run_validators(errors, 'sample_sent', obj.sample_sent, [required])

    if obj.sample_sent:
        run_validators(errors, 'sample_sent_date', obj.sample_sent_date, [required])