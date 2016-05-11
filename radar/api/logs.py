from flask import request

from radar.auth.sessions import current_user, get_user_agent, get_ip_address
from radar.database import db
from radar.models.logs import Log
from radar.models.users import User


def get_user(session):
    if current_user.is_authenticated():
        user = session.query(User).get(current_user.id)
    else:
        user = None

    return user


def get_url():
    url = request.path

    if request.query_string:
        url = url + '?' + request.query_string

    return url


# TODO this isn't called when a exception is raised (status_code = 500)
def log_request(response):
    session = db.session.session_factory()

    log = Log()
    log.type = 'API'
    log.user = get_user(session)
    log.data = dict(
        method=request.method,
        url=get_url(),
        status_code=response.status_code,
        user_agent=get_user_agent(),
        ip_address=get_ip_address()
    )
    session.add(log)

    session.commit()

    return response


def log_view_patients(patients):
    for patient in patients:
        log_view_patient(patient)


def log_view_patient(patient):
    session = db.session.session_factory()

    log = Log()
    log.type = 'VIEW_PATIENT'
    log.user = get_user(session)
    log.data = dict(
        patient_id=patient.id,
    )
    session.add(log)

    session.commit()
