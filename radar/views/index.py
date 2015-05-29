from flask import render_template, Blueprint

from radar.models.news import Story
from radar.lib.forms.auth import LoginForm


bp = Blueprint('radar', __name__)


@bp.route('/')
def index():
    login_form = LoginForm()

    stories = Story.query.order_by(Story.published.desc()).limit(3).all()

    context = dict(
        login_form=login_form,
        stories=stories,
    )

    return render_template('index.html', **context)