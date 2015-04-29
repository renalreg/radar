from flask import Blueprint

bp = Blueprint('diagnosis', __name__)

@bp.route('/<int:disease_group_id>')
def view_diagnosis():
    pass