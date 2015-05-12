from flask import Blueprint


bp = Blueprint('transplants', __name__)


@bp.route('/')
def view_transplant_list(patient_id):
    pass


@bp.route('/<int:transplant_id>/')
def view_transplant(patient_id, transplant_id):
    pass