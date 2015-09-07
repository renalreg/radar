from radar.api.serializers.posts import PostSerializer
from radar.lib.views import ListCreateApiView, RetrieveUpdateDestroyAPIView
from radar.models import Post


class PostList(ListCreateApiView):
    serializer_class = PostSerializer
    model_class = Post


class PostDetail(RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    model_class = Post
