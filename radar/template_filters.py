from cornflake.utils import safe_strftime
from jinja2 import escape, evalcontextfilter, Markup


def safe_strftime_template_filter(value, format):
    if value is None:
        return ''
    else:
        return safe_strftime(value, format)


@evalcontextfilter
def nl2br_template_filter(eval_ctx, value):
    if value is None:
        return ''

    value = escape(value)
    value = value.replace('\n', Markup('<br />\n'))

    if eval_ctx.autoescape:
        value = Markup(value)

    return value


def register_template_filters(app):
    app.add_template_filter(safe_strftime_template_filter, 'safe_strftime')
    app.add_template_filter(nl2br_template_filter, 'nl2br')
