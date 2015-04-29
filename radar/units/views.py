from flask_login import current_user
from flask import render_template, Blueprint

from radar.models import Unit
from radar.users.models import UnitUser
from radar.users.roles import UNIT_GOD


bp = Blueprint('units', __name__)


@bp.route('/')
def list_units():
    if current_user.is_admin:
        units = Unit.query.order_by(Unit.name).all()
        units = [(x, None) for x in units]
    else:
        unit_memberships = UnitUser.query\
            .join(UnitUser.unit)\
            .filter(UnitUser.user == current_user)\
            .order_by(Unit.name)\
            .all()

        units = [(x.unit, x) for x in unit_memberships]

    context = dict(
        units=units,
    )

    return render_template('units.html', **context)


@bp.route('/<int:unit_id>/')
def view_unit(unit_id):
    if current_user.is_admin:
        unit = Unit.query.get_or_404(unit_id)
        unit_user = UnitUser(unit=unit, user=current_user, role=UNIT_GOD)
    else:
        unit_user = UnitUser.query\
            .filter(UnitUser.user == current_user)\
            .filter(UnitUser.unit_id == unit_id)\
            .first_or_404()

    context = dict(
        unit=unit_user.unit,
        unit_user=unit_user
    )

    return render_template('unit.html', **context)