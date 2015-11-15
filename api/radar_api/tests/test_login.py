import json

from radar_api.tests.helpers import e2e
from radar.database import db
from radar.models.users import User


@e2e
def test_login(client):
    user = User()
    user.username = 'admin'
    user.password = 'password'
    db.session.add(user)
    db.session.commit()

    response = client.post(
        '/login',
        content_type='application/json',
        data=json.dumps({
            'username': 'admin',
            'password': 'password'
        }),
        environ_base={
            'REMOTE_ADDR': '127.0.0.1'
        }
    )

    assert response.status_code == 200
