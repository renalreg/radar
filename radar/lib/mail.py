from flask import current_app
from flask_mail import Mail as BaseMail


class Mail(BaseMail):
    def send(self, message):
        if current_app.debug:
            print message

        super(Mail, self).send(message)

mail = Mail()