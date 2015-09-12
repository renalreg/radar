from sqlalchemy import func
from radar.lib.validation.core import Field, pass_context, pass_old_obj
from radar.lib.validation.validators import required


class CreatedUserField(Field):
    @pass_context
    @pass_old_obj
    def pre_validate(self, ctx, old_created_user, new_created_user):
        user = ctx['user']

        if old_created_user is None:
            new_created_user = user

        return new_created_user


class ModifiedUserField(Field):
    @pass_context
    def pre_validate(self, ctx, modified_user):
        user = ctx['user']
        return user


class CreatedDateField(Field):
    @pass_old_obj
    def pre_validate(self, old_created_date, new_created_date):
        if old_created_date is None:
            new_created_date = func.now()

        return new_created_date


class ModifiedDateField(Field):
    def pre_validate(self, created_date):
        return func.now()


class CreatedValidationMixin(object):
    created_user = CreatedUserField(chain=[required()])
    created_date = CreatedDateField(chain=[required()])


class ModifiedValidationMixin(object):
    modified_user = ModifiedUserField(chain=[required()])
    modified_date = ModifiedDateField(chain=[required()])


class MetaValidationMixin(CreatedValidationMixin, ModifiedValidationMixin):
    pass
