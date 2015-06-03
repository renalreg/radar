from flask import render_template


def page_not_found(error):
    return render_template('404.html')


def forbidden(error):
    return render_template('403.html')
