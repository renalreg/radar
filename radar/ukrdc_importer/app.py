from sqlalchemy import event

from radar.app import Radar
from radar.database import db
from radar.ukrdc_importer.utils import get_import_user


class RadarUKRDCImporter(Radar):
    def __init__(self, *args, **kwargs):
        super(RadarUKRDCImporter, self).__init__(*args, **kwargs)

        @event.listens_for(db.session, 'before_flush')
        def before_flush(session, flush_context, instances):
            user = get_import_user()

            # SET LOCAL lasts until the end of the current transaction
            # http://www.postgresql.org/docs/9.4/static/sql-set.html
            session.execute('SET LOCAL radar.user_id = :user_id', dict(user_id=user.id))
