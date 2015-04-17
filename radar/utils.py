def humanize_datetime_format(datetime_format):
    output = datetime_format.replace('%d', 'DD')
    output = output.replace('%m', 'MM')
    output = output.replace('%Y', 'YYYY')
    return output

def date_format_to_javascript(date_format):
    output = date_format.replace('%d', 'dd')
    output = output.replace('%m', 'mm')
    output = output.replace('%Y', 'yy')
    return output