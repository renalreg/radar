from math import ceil
from flask import request, abort, url_for
from flask_sqlalchemy import Pagination


def page_from_request():
    page = request.args.get('page')

    if page is None:
        return 1

    try:
        page = int(page)
    except ValueError:
        abort(404)

    if page < 1:
        abort(404)

    return page


def per_page_from_request(default):
    page = request.args.get('per_page')

    if page is None:
        return default

    try:
        page = int(page)
    except ValueError:
        abort(404)

    if page == -1:
        return None

    if page < 1:
        abort(404)

    return page


def paginate_query(query, default_per_page=20):
    page = page_from_request()
    per_page = per_page_from_request(default=default_per_page)

    if per_page is None:
        total_count = query.count()
        pagination = Pagination(query, 1, total_count, total_count, query.all())
    else:
        pagination = query.paginate(page, per_page)

    return pagination


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