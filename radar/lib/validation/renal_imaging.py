from radar.lib.validation.core import run_validators
from radar.lib.validation.patient_validators import after_date_of_birth
from radar.lib.validation.validators import required, in_, range_, not_in_future


def validate_renal_imaging(errors, obj):
    patient = obj.patient

    run_validators(errors, 'date', obj.date, [required, after_date_of_birth(patient), not_in_future])
    run_validators(errors, 'imaging_type', obj.imaging_type, [required])
    run_validators(errors, 'right_present', obj.right_present, [required])
    run_validators(errors, 'left_present', obj.left_present, [required])

    if obj.right_present:
        run_validators(errors, 'right_type', obj.right_type, [required, in_(['transplant', 'natural'])])
        run_validators(errors, 'right_length', obj.right_length, [required, range_(0, 100)])  # TODO range
        run_validators(errors, 'right_cysts', obj.right_cysts, [required])
        run_validators(errors, 'right_calcification', obj.right_calcification, [required])

        if obj.right_calcification:
            run_validators(errors, 'right_nephrocalcinosis', obj.right_nephrocalcinosis, [required])
            run_validators(errors, 'right_nephrolithiasis', obj.right_nephrolithiasis, [required])
        else:
            obj.right_nephrocalcinosis = None
            obj.right_nephrolithiasis = None
    else:
        obj.right_type = None
        obj.right_length = None
        obj.right_cysts = None
        obj.right_calcification = None
        obj.right_nephrocalcinosis = None
        obj.right_nephrolithiasis = None

    if obj.left_present:
        run_validators(errors, 'left_type', obj.left_type, [required, in_(['transplant', 'natural'])])
        run_validators(errors, 'left_length', obj.left_length, [required, range_(0, 100)])  # TODO range
        run_validators(errors, 'left_cysts', obj.left_cysts, [required])
        run_validators(errors, 'left_calcification', obj.left_calcification, [required])

        if obj.left_calcification:
            run_validators(errors, 'left_nephrocalcinosis', obj.left_nephrocalcinosis, [required])
            run_validators(errors, 'left_nephrolithiasis', obj.left_nephrolithiasis, [required])
        else:
            obj.left_nephrocalcinosis = None
            obj.left_nephrolithiasis = None
    else:
        obj.left_type = None
        obj.left_length = None
        obj.left_cysts = None
        obj.left_calcification = None
        obj.left_nephrocalcinosis = None
        obj.left_nephrolithiasis = None
