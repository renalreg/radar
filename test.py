from datetime import datetime
import pytz
from radar.app import create_app
from dateutil.parser import parse
from radar.database import db
from radar.models import Foo

app = create_app('settings.py')

with app.app_context():
    Foo.query.delete()

    foo = Foo()
    dt = parse('2015-06-01T17:36:39Z')
    foo.date_1 = dt
    foo.date_2 = dt
    db.session.add(foo)

    bar = Foo()
    dt = datetime(2015, 6, 1, 17, 36, 39)
    bar.date_1 = dt
    bar.date_2 = dt
    db.session.add(bar)

    db.session.commit()

    for foo in Foo.query.all():
        print foo.id, foo.date_1, foo.date_2

