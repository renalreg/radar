from flask_login import current_user
from radar.models import CreatedModifiedMixin


def receive_before_flush(session, flush_context, instances):
    """ Sets the created user and modified user fields """

    _ = flush_context, instances

    for obj in session.new:
        if isinstance(obj, CreatedModifiedMixin):
            if obj.created_user is None:
                obj.created_user = current_user

            obj.modified_user = current_user

    for obj in session.dirty:
        if isinstance(obj, CreatedModifiedMixin):
            obj.modified_user = current_user