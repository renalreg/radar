from flask import render_template
from flask_mail import Message

from radar.mail import mail


def send_new_user_email(user, password):
    # TODO
    login_url = 'TODO'
    msg = Message('RaDaR New User', recipients=[user.email])
    msg.html = render_template('emails/new_user.html', user=user, password=password, login_url=login_url)
    mail.send(msg)
