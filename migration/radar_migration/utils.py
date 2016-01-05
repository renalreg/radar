def clean(value):
    value = value.replace("\x92", "'")
    return value
