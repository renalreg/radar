from radar.lib.serializers import MetaSerializerMixin, ModelSerializer
from radar.lib.views import ListCreateApiView, RetrieveUpdateDestroyAPIView
from radar.models import Post


class PostSerializer(MetaSerializerMixin, ModelSerializer):
    class Meta:
        model_class = Post


class PostList(ListCreateApiView):
    serializer_class = PostSerializer
    model_class = Post


class PostDetail(RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    model_class = Post
