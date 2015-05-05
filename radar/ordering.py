from flask import request, abort, url_for
from sqlalchemy import desc, Sequence


ASCENDING = 'asc'
DESCENDING = 'desc'


def order_by_from_request(default, columns):
    order_by = request.args.get('order_by')

    if order_by is None:
        return default
    elif order_by in columns:
        return order_by
    else:
        abort(404)


def order_direction_from_request(default):
    order_direction = request.args.get('order_direction')

    if order_direction is None:
        return default
    elif order_direction == ASCENDING:
        return ASCENDING
    elif order_direction == DESCENDING:
        return DESCENDING
    else:
        abort(404)


def ordering_from_request(columns, default_order_by=None, default_order_direction=ASCENDING):
    order_by = order_by_from_request(default_order_by, columns)
    order_direction = order_direction_from_request(default=default_order_direction)
    ordering = Ordering(order_by, order_direction)
    return ordering


def order_query(query, order_by_map, default_order_by=None, default_order_direction=ASCENDING):
    ordering = order_by_from_request(order_by_map.keys(), default_order_by, default_order_direction)

    clauses = order_by_map[ordering.column]

    if not isinstance(clauses, list):
        clauses = [clauses]

    if ordering.direction == DESCENDING:
        clauses = [desc(x) for x in clauses]

    return query.order_by(*clauses), ordering


class Ordering(object):
    def __init__(self, column, direction):
        self.column = column
        self.direction = direction

    def reverse(self, column):
        if self.column == column:
            if self.direction == ASCENDING:
                return DESCENDING
            else:
                return ASCENDING

        return ASCENDING

    def is_ordered_by(self, column):
        return self.column == column

    @property
    def is_ascending(self):
        return self.direction == ASCENDING


def url_for_order_by(order_by, order_direction):
    args = request.args.to_dict()
    args.update(request.view_args)

    # Back to the first page
    args.pop('page', None)

    args['order_by'] = order_by
    args['order_direction'] = order_direction

    return url_for(request.endpoint, **args)