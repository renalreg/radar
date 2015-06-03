from flask_login import current_user
from flask import render_template, Blueprint, request, jsonify

from radar.lib.news import get_latest_news
from radar.models.disease_groups import DiseaseGroup, DiseaseGroupPatient, DiseaseGroupUser
from radar.lib.recruitment_stats import recruitment_by_month
from radar.lib.roles import DISEASE_GROUP_GOD

bp = Blueprint('disease_groups', __name__)


@bp.route('/')
def list_disease_groups():
    if current_user.is_admin:
        disease_groups = DiseaseGroup.query.order_by(DiseaseGroup.name).all()
        disease_groups = [(x, None) for x in disease_groups]
    else:
        disease_group_memberships = DiseaseGroupUser.query\
            .join(DiseaseGroupUser.disease_group)\
            .filter(DiseaseGroupUser.user == current_user)\
            .order_by(DiseaseGroup.name)\
            .all()

        disease_groups = [(x.disease_group, x) for x in disease_group_memberships]

    context = dict(
        disease_groups=disease_groups,
    )

    return render_template('disease_groups.html', **context)


@bp.route('/<int:disease_group_id>/')
def view_disease_group(disease_group_id):
    disease_group_user = get_disease_group_user(disease_group_id)

    posts = get_latest_news()

    context = dict(
        disease_group=disease_group_user.disease_group,
        disease_group_user=disease_group_user,
        posts=posts,
    )

    return render_template('disease_group.html', **context)


@bp.route('/<int:disease_group_id>/recruitment.json')
def recruitment_json(disease_group_id):
    cumulative = request.args.get('cumulative') == '1'

    disease_group_user = get_disease_group_user(disease_group_id)

    data = recruitment_by_month(
        DiseaseGroupPatient.created_date,
        [DiseaseGroupPatient.disease_group == disease_group_user.disease_group],
        cumulative=cumulative
    )

    return jsonify(data=[{'date': x[0].isoformat(), 'count': x[1]} for x in data])


def get_disease_group_user(disease_group_id):
    if current_user.is_admin:
        disease_group = DiseaseGroup.query.get_or_404(disease_group_id)
        disease_group_user = DiseaseGroupUser(disease_group=disease_group, user=current_user, role=DISEASE_GROUP_GOD)
    else:
        disease_group_user = DiseaseGroupUser.query\
            .filter(DiseaseGroupUser.user == current_user)\
            .filter(DiseaseGroupUser.disease_group_id == disease_group_id)\
            .first_or_404()

    return disease_group_user
