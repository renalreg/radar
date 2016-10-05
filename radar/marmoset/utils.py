def identity(value):
    return value


def wrap(value):
    def wrapper(*args, **kwargs):
        return value

    return wrapper
