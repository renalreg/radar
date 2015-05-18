from flask_login import current_user
from radar.disease_groups.services import get_disease_groups_for_user
from radar.forms import DeleteForm
from radar.units.services import get_units_for_user


def inject_navigation():
        navigation = dict()

        if current_user.is_authenticated():
            navigation['units'] = get_units_for_user(current_user)
            navigation['disease_groups'] = get_disease_groups_for_user(current_user)

        return dict(navigation=navigation)

def inject_delete_form():
    return dict(delete_form=DeleteForm())