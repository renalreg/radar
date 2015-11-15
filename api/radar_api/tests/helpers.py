import pytest


def e2e(f):
    f = pytest.mark.e2e(f)
    f = pytest.mark.usefixtures('transaction')(f)
    return f
