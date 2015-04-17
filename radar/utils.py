# TODO complete
def humanize_datetime_format(datetime_format):
    output = datetime_format.replace('%d', 'DD')
    output = output.replace('%m', 'MM')
    output = output.replace('%Y', 'YYYY')
    return output