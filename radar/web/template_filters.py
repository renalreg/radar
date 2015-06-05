from jinja2 import escape, Markup, evalcontextfilter
from radar.lib.utils import date_to_datetime
from datetime import date


def strftime(dt, dt_format):
    if dt is None:
        return ''
    else:
        return dt.strftime(dt_format)


def year_format(dt):
    if dt is None:
        return ''
    else:
        return '%04d' % dt.year


def date_format(dt):
    if dt is None:
        return ''
    else:
        return '%02d/%02d/%04d' % (dt.day, dt.month, dt.year)


def datetime_format(dt, seconds=False):
    if dt is None:
        return ''
    else:
        if isinstance(dt, date):
            dt = date_to_datetime(dt)

        output = '%02d/%02d/%04d %02d:%02d' % (dt.day, dt.month, dt.year, dt.hour, dt.minute)

        if seconds:
            output += ':%02d' % dt.second

        return output


@evalcontextfilter
def nl2br(eval_ctx, value):
    value = escape(value)
    value = value.replace('\n', Markup('<br />\n'))

    if eval_ctx.autoescape:
        value = Markup(value)

    return value


def missing(value):
    if value is None or value == '':
        return '-'
    else:
        return value


def yn(value):
    if value is None:
        return None
    elif value:
        return 'Yes'
    else:
        return 'No'
