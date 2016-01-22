from flask import Flask

from radar.database import db
from radar.config import check_config


def create_app(config=None):
    app = Flask(__name__)
    app.config.from_object('radar.default_settings')

    if config is not None:
        app.config.update(config)

    check_config(app.config)

    # noinspection PyUnresolvedReferences
    from radar import models  # noqa

    db.init_app(app)

    return app
