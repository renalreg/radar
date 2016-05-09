def test_forgot_username(app):
    client = app.test_client()

    response = client.post('/forgot-username', data={
        'email': 'foo@example.org'
    })

    assert response.status_code == 200


def test_email_missing(app):
    client = app.test_client()

    response = client.post('/forgot-username', data={})

    assert response.status_code == 422


def test_user_not_found(app):
    client = app.test_client()

    response = client.post('/forgot-username', data={
        'email': '404@example.org'
    })

    assert response.status_code == 422
