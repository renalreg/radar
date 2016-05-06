from datetime import datetime

import pytz
from cornflake.sqlalchemy_orm import ModelSerializer
from cornflake import fields
from cornflake.validators import not_empty, sanitize_html

from radar.models.posts import Post


class PostSerializer(ModelSerializer):
    title = fields.StringField(validators=[not_empty()])
    published_date = fields.DateTimeField(default=lambda: datetime.now(pytz.utc))
    body = fields.StringField(validators=[not_empty(), sanitize_html()])

    class Meta(object):
        model_class = Post
