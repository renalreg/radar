from datetime import datetime

from cornflake import fields
from cornflake.sqlalchemy_orm import ModelSerializer
from cornflake.validators import not_empty, sanitize_html
import pytz

from radar.api.serializers.common import MetaMixin
from radar.models.posts import Post


class PostSerializer(ModelSerializer):
    title = fields.StringField(validators=[not_empty()])
    published_date = fields.DateTimeField(default=lambda: datetime.now(pytz.utc))
    body = fields.StringField(validators=[not_empty(), sanitize_html()])

    class Meta(object):
        model_class = Post
        exclude = ["created_user_id", "modified_user_id"]


class PostAuthorSerializer(MetaMixin, PostSerializer):
    pass
