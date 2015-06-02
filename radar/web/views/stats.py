from flask import render_template, Blueprint

bp = Blueprint('stats', __name__)


@bp.route('/')
def view_stats():
    return render_template('stats.html')