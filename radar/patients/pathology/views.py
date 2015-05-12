from flask import Blueprint


bp = Blueprint('pathology', __name__)


@bp.route('/')
def view_pathology_list(patient_id):
    pass