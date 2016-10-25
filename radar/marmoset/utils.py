def identity(value):
    return value


def wrap(value):
    """Create a function that returns the specified value."""

    def wrapper(*args, **kwargs):
        return value

    return wrapper
