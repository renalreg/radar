from flask_login import current_user
from flask import render_template, Blueprint, jsonify, request

from radar.models.patients import UnitPatient
from radar.models.news import Story
from radar.patients.stats import recruitment_by_month
from radar.models.units import Unit
from radar.models.users import UnitUser
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
    unit_user = get_unit_user(unit_id)

    stories = Story.query.order_by(Story.published.desc()).limit(1).all()

    context = dict(
        unit=unit_user.unit,
        unit_user=unit_user,
        stories=stories,
    )

    return render_template('unit.html', **context)


@bp.route('/<int:unit_id>/recruitment.json')
def recruitment_json(unit_id):
    cumulative = request.args.get('cumulative') == '1'

    unit_user = get_unit_user(unit_id)

    data = recruitment_by_month(UnitPatient.created_date, [UnitPatient.unit == unit_user.unit], cumulative=cumulative)

    return jsonify(data=[{'date': x[0].isoformat(), 'count': x[1]} for x in data])


def get_unit_user(unit_id):
    if current_user.is_admin:
        unit = Unit.query.get_or_404(unit_id)
        unit_user = UnitUser(unit=unit, user=current_user, role=UNIT_GOD)
    else:
        unit_user = UnitUser.query\
            .filter(UnitUser.user == current_user)\
            .filter(UnitUser.unit_id == unit_id)\
            .first_or_404()

    return unit_user