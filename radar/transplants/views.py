from flask import Blueprint


bp = Blueprint('transplants', __name__)


@bp.route('/')
def view_transplant_list(patient_id):
    pass