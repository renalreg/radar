from radar.models import User
from radar.validation.utils import VALIDATIONS
from radar.database import db


def validate_and_add(obj, ctx=None):
    # Queries run during validation can cause a premature flush
    with db.session.no_autoflush:
        model_class = obj.__class__
        validation_class = VALIDATIONS[model_class]
        obj = validation_runner(model_class, validation_class, obj, ctx)

    db.session.add(obj)
    db.session.flush()

    return obj


def validation_runner(model_class, validation_class, obj, ctx=None):
    if ctx is None:
        ctx = {}

    validation = validation_class()

    if ctx.get('user') is None:
        ctx['user'] = User.query.filter(User.username == 'bot').one()

    validation.before_update(ctx, model_class())
    old_obj = validation.clone(obj)
    obj = validation.after_update(ctx, old_obj, obj)

    return obj
