from flask import Blueprint


bp = Blueprint('hospitalisation', __name__)


@bp.route('/')
def view_hospitalisation_list(patient_id):
    pass