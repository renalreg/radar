from flask import Blueprint


bp = Blueprint('plasmapheresis', __name__)


@bp.route('/')
def view_plasmapheresis_list(patient_id):
    pass