from datetime import datetime

from cornflake.exceptions import ValidationError
from freezegun import freeze_time
import pytest
import pytz

from radar.api.serializers.posts import PostSerializer
from radar.models.users import User


@pytest.fixture
def post():
    return {
        'title': 'Hello',
        'body': '<p>This is a test!</p>',
        'published_date': datetime(2000, 1, 2, tzinfo=pytz.UTC)
    }


def test_valid(post):
    obj = valid(post)

    assert obj.title == 'Hello'
    assert obj.body == '<p>This is a test!</p>'
    assert obj.published_date == datetime(2000, 1, 2, tzinfo=pytz.UTC)

    assert obj.created_date is not None
    assert obj.modified_date is not None
    assert obj.created_user is not None
    assert obj.modified_user is not None


def test_title_missing(post):
    post['title'] = None
    invalid(post)


def test_title_blank(post):
    post['title'] = ''
    invalid(post)


def test_body_missing(post):
    post['body'] = None
    invalid(post)


def test_body_blank(post):
    post['body'] = ''
    invalid(post)


@freeze_time("2000-01-02")
def test_published_date_missing(post):
    post['published_date'] = None
    obj = valid(post)
    assert obj.published_date == datetime(2000, 1, 2, tzinfo=pytz.UTC)


def invalid(data):
    with pytest.raises(ValidationError) as e:
        valid(data)

    return e


def valid(data):
    serializer = PostSerializer(data=data, context={'user': User(is_admin=True)})
    serializer.is_valid(raise_exception=True)
    return serializer.save()
