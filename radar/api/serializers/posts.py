from radar.lib.serializers import MetaSerializerMixin, ModelSerializer
from radar.models import Post


class PostSerializer(MetaSerializerMixin, ModelSerializer):
    class Meta:
        model_class = Post
