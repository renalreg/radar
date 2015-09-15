from radar.api.serializers.meta import MetaSerializerMixin
from radar.lib.serializers import ModelSerializer
from radar.lib.models import Post


class PostSerializer(MetaSerializerMixin, ModelSerializer):
    class Meta(object):
        model_class = Post
