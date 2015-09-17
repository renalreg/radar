from radar.lib.models import User


def validation_runner(model_class, validation_class, obj, is_admin=True, user=None, old_obj=None):
    if user is None:
        user = User(is_admin=is_admin)

    if old_obj is None:
        old_obj = model_class()

    validation = validation_class()
    ctx = {'user': user}
    validation.before_update(ctx, old_obj)
    old_obj = validation.clone(old_obj)
    obj = validation.after_update(ctx, old_obj, obj)
    return obj
