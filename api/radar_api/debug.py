import time

from collections import defaultdict

from flask_sqlalchemy import get_debug_queries
from flask import g


def foo():
    g.start = time.time()


def bar(exception):
    print '%.2f seconds' % (time.time() - g.start)

    total_duration = 0

    queries = defaultdict(lambda: [0, 0])

    for q in get_debug_queries():
        queries[q.statement][0] += 1
        queries[q.statement][1] += q.duration
        total_duration += q.duration

    queries = [(k, v[0], v[1]) for k, v in queries.items()]
    queries = [x for x in queries if x[2] >= 0.1]
    queries.sort(key=lambda x: x[1], reverse=True)

    for statement, times_run, total_duration in queries:
        print '%.2f seconds (%d): %s' % (total_duration, times_run, statement)
