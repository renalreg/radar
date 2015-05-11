from flask_login import current_user
from flask import render_template, Blueprint

from radar.disease_groups.models import DiseaseGroup
from radar.news.models import Story
from radar.users.models import DiseaseGroupUser
from radar.users.roles import DISEASE_GROUP_GOD


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
    if current_user.is_admin:
        disease_group = DiseaseGroup.query.get_or_404(disease_group_id)
        disease_group_user = DiseaseGroupUser(disease_group=disease_group, user=current_user, role=DISEASE_GROUP_GOD)
    else:
        disease_group_user = DiseaseGroupUser.query\
            .filter(DiseaseGroupUser.user == current_user)\
            .filter(DiseaseGroupUser.disease_group_id == disease_group_id)\
            .first_or_404()

    stories = Story.query.order_by(Story.published.desc()).limit(1).all()

    context = dict(
        disease_group=disease_group_user.disease_group,
        disease_group_user=disease_group_user,
        stories=stories,
    )

    return render_template('disease_group.html', **context)