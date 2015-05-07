from flask import render_template, Blueprint
from radar.users.forms import LoginForm


bp = Blueprint('radar', __name__)

@bp.route('/')
def index():
    login_form = LoginForm()

    context = dict(
        login_form=login_form
    )

    return render_template('index.html', **context)