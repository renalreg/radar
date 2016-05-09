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

    celery = Celery()
    celery.conf.CELERY_DEFAULT_QUEUE = 'ukrdc_exporter'
    
    import radar_ukrdc_exporter.tasks  # noqa

    broker_url = app.config.get('CELERY_BROKER_URL')

    if broker_url is not None:
        celery.conf.BROKER_URL = broker_url

    celery.conf.update(app.config)

    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask

    return celery
