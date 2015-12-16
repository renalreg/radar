import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from jinja2 import Environment, PackageLoader

from radar.config import get_config_value

COMMA_SPACE = ', '

env = Environment(
    loader=PackageLoader('radar', 'templates/emails'),
    trim_blocks=True,
    lstrip_blocks=True,
    autoescape=True,
)


def is_email_enabled():
    return get_config_value('EMAIL_ENABLED')


def get_email_from_address():
    return get_config_value('EMAIL_FROM_ADDRESS')


def get_email_smtp_host():
    return get_config_value('EMAIL_SMTP_HOST')


def get_email_smtp_port():
    return get_config_value('EMAIL_SMTP_PORT')


def get_smtp():
    smtp_host = get_email_smtp_host()
    smtp_port = get_email_smtp_port()
    s = smtplib.SMTP(smtp_host, smtp_port)
    return s


def send_email(to_addresses, subject, message_plain, message_html=None, from_address=None):
    if from_address is None:
        from_address = get_email_from_address()

    if not isinstance(to_addresses, list):
        to_addresses = [to_addresses]

    email_enabled = is_email_enabled()

    m = MIMEMultipart('alternative')
    m['Subject'] = subject
    m['From'] = from_address
    m['To'] = COMMA_SPACE.join(to_addresses)

    m_plain = MIMEText(message_plain, 'plain')
    m.attach(m_plain)

    if message_html is not None:
        m_html = MIMEText(message_html, 'html')
        m.attach(m_html)

    if email_enabled:
        s = get_smtp()
        s.sendmail(from_address, to_addresses, m.as_string())
        s.quit()
    else:
        print m.as_string()


def send_email_from_template(to_addresses, subject, template_name, context, from_address=None):
    template_plain = env.get_template('%s.txt' % template_name)
    message_plain = template_plain.render(**context)

    template_html = env.get_template('%s.html' % template_name)
    message_html = template_html.render(**context)

    send_email(
        to_addresses,
        subject,
        message_plain,
        message_html=message_html,
        from_address=from_address
    )
