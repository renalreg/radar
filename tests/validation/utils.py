from radar.lib.models import User


def validation_runner(model_class, validation_class, obj, is_admin=True):
    validation = validation_class()
    ctx = {'user': User(is_admin=is_admin)}
    validation.before_update(ctx, model_class())
    old_obj = validation.clone(obj)
    obj = validation.after_update(ctx, old_obj, obj)
    return obj
