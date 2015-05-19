from itertools import chain

from flask_login import current_user
from radar.models import CreatedMixin, ModifiedMixin


def before_flush_set_created_listener(session, flush_context, instances):
    """ Sets the created user field """

    _ = flush_context, instances

    for obj in session.new:
        if isinstance(obj, CreatedMixin):
            if obj.created_user is None:
                obj.created_user = current_user


def before_flush_set_modified_listener(session, flush_context, instances):
    """ Sets the modified user field """

    _ = flush_context, instances

    for obj in chain(session.new, session.dirty):
        if isinstance(obj, ModifiedMixin):
            obj.modified_user = current_user