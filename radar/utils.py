from datetime import datetime

from flask import request, url_for


def humanize_datetime_format(datetime_format):
    output = datetime_format.replace('%d', 'DD')
    output = output.replace('%m', 'MM')
    output = output.replace('%Y', 'YYYY')
    return output


def date_format_to_javascript(date_format):
    output = date_format.replace('%d', 'dd')
    output = output.replace('%m', 'mm')
    output = output.replace('%Y', 'yy')
    return output


def url_for_page(page):
    args = request.args.copy()
    args.update(request.view_args)

    args['page'] = page

    return url_for(request.endpoint, **args)


def url_for_per_page(per_page):
    args = request.args.copy()
    args.update(request.view_args)

    args['page'] = 1
    args['per_page'] = per_page

    return url_for(request.endpoint, **args)


def url_for_order_by(order_by, order_direction):
    args = request.args.copy()
    args.update(request.view_args)

    args['page'] = 1
    args['order_by'] = order_by
    args['order_direction'] = order_direction

    return url_for(request.endpoint, **args)


def current_order_by():
    return request.args.get('order_by')


def current_order_direction():
    return request.args.get('order_direction', 'asc')


def get_path(data, *keys):
    for key in keys:
        data = data.get(key)

        if data is None:
            return None

    return data


def get_path_as_datetime(data, *keys):
    value = get_path(data, *keys)

    if value is not None:
        value = datetime.strptime(value, '%Y-%m-%dT%H:%M:%SZ')

    return value