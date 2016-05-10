def test_forgot_username(api):
    client = api.test_client()

    response = client.post('/forgot-username', data={
        'email': 'foo@example.org'
    })

    assert response.status_code == 200


def test_email_missing(api):
    client = api.test_client()

    response = client.post('/forgot-username', data={})

    assert response.status_code == 422


def test_user_not_found(api):
    client = api.test_client()

    response = client.post('/forgot-username', data={
        'email': '404@example.org'
    })

    assert response.status_code == 422
