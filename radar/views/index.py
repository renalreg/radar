from flask import render_template, Blueprint
from radar.lib.news import get_latest_news

from radar.models.news import Post
from radar.lib.forms.auth import LoginForm


bp = Blueprint('radar', __name__)


@bp.route('/')
def index():
    login_form = LoginForm()

    posts = get_latest_news()

    context = dict(
        login_form=login_form,
        posts=posts,
    )

    return render_template('index.html', **context)