from flask import Flask
from celery import Celery

from radar.database import db


def create_app():
    app = Flask(__name__)
    app.config.from_envvar('RADAR_SETTINGS')

    # noinspection PyUnresolvedReferences
    from radar import models  # noqa

    db.init_app(app)

    return app


def create_celery(app=None):
    if app is None:
        app = create_app()

    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)

    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask

    return celery
