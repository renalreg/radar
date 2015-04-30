def add_errors_to_form(form, errors):
    for field, field_errors in errors:
        getattr(form, field).errors.extend(field_errors)