from radar.lib.permissions import IsAdminOrReadOnly
from radar.lib.serializers import MetaSerializerMixin, ModelSerializer
from radar.lib.views import ListCreateApiView
from radar.models import Post


class PostSerializer(MetaSerializerMixin, ModelSerializer):
    class Meta:
        model = Post


class PostList(ListCreateApiView):
    serializer_class = PostSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_query(self):
        return Post.query


class PostDetail(ListCreateApiView):
    serializer_class = PostSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_query(self):
        return Post.query
