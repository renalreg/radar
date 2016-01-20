import time
from collections import defaultdict

from flask_sqlalchemy import get_debug_queries
from flask import g
from termcolor import colored


def debug_before_request():
    g.start = time.time()


def debug_teardown_request(exception):
    response_time = time.time() - g.start

    if response_time >= 0.1:
        print colored('slow response (%.2f seconds)' % response_time, 'yellow')

    total_query_time = 0

    queries = defaultdict(lambda: [0, 0])

    for q in get_debug_queries():
        queries[q.statement][0] += 1
        queries[q.statement][1] += q.duration
        total_query_time += q.duration

    # Queries taking longer than 0.1 seconds (slowest first)
    queries = [(k, v[0], v[1]) for k, v in queries.items()]
    queries = [x for x in queries if x[2] >= 0]
    queries.sort(key=lambda x: x[1], reverse=True)

    for query, times_run, query_time in queries:
        if times_run > 1:
            message = 'slow query ({2:.2f} seconds over {1} calls) - {0}'
        else:
            message = 'slow query ({2:.2f} seconds) - {0}'

        print colored(message.format(query, times_run, query_time), 'yellow')
