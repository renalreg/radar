from jinja2 import escape, Markup, evalcontextfilter


def date_format(d, date_format='%d/%m/%Y'):
    return datetime_format(d, date_format)


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