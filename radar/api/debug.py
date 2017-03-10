from __future__ import print_function
from collections import defaultdict
import time

from flask import g, request
from flask_sqlalchemy import get_debug_queries
from termcolor import colored


def debug_before_request():
    """Used by debug_teardown_request to time the request."""

    g.start = time.time()


def debug_teardown_request(exception):
    """Log slow responses and queries."""

    url = request.url

    response_time = time.time() - g.start

    if response_time >= 0.1:
        msg = '{url} - slow response ({response_time:.2f} seconds)'
        print(colored(msg.format(url=url, response_time=response_time), 'yellow'))

    total_query_time = 0

    queries = defaultdict(lambda: [0, 0])

    for q in get_debug_queries():
        queries[q.statement][0] += 1  # number of time query run
        queries[q.statement][1] += q.duration  # total time for query
        total_query_time += q.duration  # total time for all queries

    # Queries taking longer than 0.1 seconds (slowest first)
    queries = [(k, v[0], v[1]) for k, v in queries.items()]
    queries = [x for x in queries if x[2] >= 0.1]
    queries.sort(key=lambda x: x[1], reverse=True)

    for query, times_run, query_time in queries:
        if times_run > 1:
            message = '{url} - slow query ({query_time:.2f} seconds over {times_run} calls) - {query}'
        else:
            message = '{url} - slow query ({query_time:.2f} seconds) - {query}'

        print(colored(message.format(url=url, query=query, times_run=times_run, query_time=query_time), 'yellow'))
