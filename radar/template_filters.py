from jinja2 import escape, Markup, evalcontextfilter
import re

_paragraph_re = re.compile(r'(?:\r\n|\r|\n){2,}')

def datetime_format(dt, datetime_format):
    if dt is None:
        return ''
    else:
        return dt.strftime(datetime_format)

@evalcontextfilter
def nl2br(eval_ctx, value):
    value = escape(value)
    value = value.replace('\n', Markup('<br />\n'))

    if eval_ctx.autoescape:
        value = Markup(value)

    return value