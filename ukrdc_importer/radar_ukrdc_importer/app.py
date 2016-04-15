from flask import Flask
from sqlalchemy import event

from radar.database import db
from radar_ukrdc_importer.utils import get_import_user


def create_app():
    app = Flask(__name__)
    app.config.from_envvar('RADAR_SETTINGS')

    # noinspection PyUnresolvedReferences
    from radar import models  # noqa

    db.init_app(app)

    @event.listens_for(db.session, 'before_flush')
    def before_flush(session, flush_context, instances):
        user = get_import_user()

        # SET LOCAL lasts until the end of the current transaction
        # http://www.postgresql.org/docs/9.4/static/sql-set.html
        session.execute('SET LOCAL radar.user_id = :user_id', dict(user_id=user.id))

    return app


def setup_celery(celery, app=None):
    if app is None:
        app = create_app()

    broker_url = app.config.get('CELERY_BROKER_URL')

    if broker_url is not None:
        celery.conf['BROKER_URL'] = broker_url

    celery.conf.update(app.config)

    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
