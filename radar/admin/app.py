from flask import Flask
from flask_admin import Admin


def create_app():
    app = Flask(__name__)
    admin = Admin(app, template_mode='bootstrap3')
    return app
