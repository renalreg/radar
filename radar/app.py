import os

from celery import Celery
from flask import Flask

from radar.config import check_config
from radar.database import db
from radar.template_filters import register_template_filters


class Radar(Flask):
    def __init__(self, config=None, **kwargs):
        super(Radar, self).__init__(__name__, **kwargs)

        self.setup_config()

        if config is not None:
            self.config.update(config)

        self.check_config()

        from radar import models  # noqa

        db.init_app(self)

        self.celery = self.setup_celery()

        register_template_filters(self)

    def setup_config(self):
        if "RADAR_SETTINGS" in os.environ:
            self.config.from_envvar("RADAR_SETTINGS")

    def check_config(self):
        check_config(self.config)

    def setup_celery(self):
        celery = Celery()

        import radar.ukrdc_importer.tasks  # noqa
        import radar.ukrdc_exporter.tasks  # noqa

        broker_url = self.config.get("CELERY_BROKER_URL")

        if broker_url is not None:
            celery.conf.BROKER_URL = broker_url

        celery.conf.update(self.config)

        TaskBase = celery.Task

        app = self

        class ContextTask(TaskBase):
            abstract = True

            def __call__(self, *args, **kwargs):
                with app.app_context():
                    return TaskBase.__call__(self, *args, **kwargs)

        celery.Task = ContextTask

        return celery
