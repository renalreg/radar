import smtplib
from email.mime.text import MIMEText, MIMEMultipart

from flask import current_app
from jinja2 import Environment, PackageLoader

COMMA_SPACE = ', '


def send_email(to_addresses, subject, message_plain, message_html=None, from_address=None):
    if from_address is None:
        from_address = current_app.config.get('FROM_ADDRESS', 'bot@radar.nhs.uk')

    send_emails = current_app.config.get('SEND_EMAILS', not current_app.debug)

    m = MIMEMultipart('alternative')
    m['Subject'] = subject
    m['From'] = from_address
    m['To'] = COMMA_SPACE.join(to_addresses)

    m_plain = MIMEText(message_plain, 'plain')
    m.attach(m_plain)

    if message_html is not None:
        m_html = MIMEText(message_html, 'html')
        m.attach(m_html)

    if send_emails:
        smtp_host = current_app.config.get('SMTP_HOST', 'localhost')
        smtp_port = current_app.config.get('SMTP_PORT', 25)

        s = smtplib.SMTP(smtp_host, smtp_port)
        s.sendmail(from_address, to_addresses, m)
        s.quit()
    else:
        print m.to_string()


def send_email_from_template(to_addresses, subject, template_name, context, from_address=None):
    env = Environment(
        loader=PackageLoader('radar', 'templates/emails'),
        trim_blocks=True,
        lstrip_blocks=True,
        autoescape=True,
    )

    template_plain = env.get_template('%s.txt' % template_name)
    message_plain = template_plain.render(**context)

    template_html = env.get_template('%s.html' % template_name)
    message_html = template_html.render(**context)

    send_email(to_addresses, subject, message_plain, message_html, from_address)
