from radar.auth.exceptions import UserNotFound
from radar.mail import send_email_from_template
from radar.models.users import User


def forgot_username(email):
    users = User.query.filter(User.email == email).all()

    # No users with that email
    if len(users) == 0:
        raise UserNotFound()

    # Send username reminder email
    send_email_from_template(email, 'RaDaR Username Reminder', 'forgot_username', {
        'email': email,
        'users': users,
    })
