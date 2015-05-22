from flask import url_for, render_template
from flask_mail import Message
from radar.disease_groups.models import DiseaseGroup
from radar.mail import mail
from radar.units.models import Unit


def get_managed_units(user):
    # TODO
    return Unit.query.order_by(Unit.name).all()


def get_managed_disease_groups(user):
    # TODO
    return DiseaseGroup.query.order_by(DiseaseGroup.name).all()


def send_new_user_email(user, password):
    login_url = url_for('auth.login', _external=True)
    msg = Message('RaDaR New User', recipients=[user.email])
    msg.html = render_template('emails/new_user.html', user=user, password=password, login_url=login_url)
    mail.send(msg)