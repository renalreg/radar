from flask import Blueprint


bp = Blueprint('dialysis', __name__)


@bp.route('/')
def view_dialysis_list(patient_id):
    pass