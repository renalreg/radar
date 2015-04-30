def add_errors_to_form(form, errors):
    for field, field_errors in errors.items():
        getattr(form, field).errors.extend(field_errors)

    # Reset cache
    form._errors = None