from radar.api.serializers.posts import PostSerializer
from radar.lib.validation.posts import PostValidation
from radar.lib.views.core import ListCreateModelView, RetrieveUpdateDestroyModelView
from radar.lib.models import Post


class PostListView(ListCreateModelView):
    serializer_class = PostSerializer
    model_class = Post
    validation_class = PostValidation
    sort_fields = ('id', 'title', 'published_date')


class PostDetailView(RetrieveUpdateDestroyModelView):
    serializer_class = PostSerializer
    model_class = Post
    validation_class = PostValidation
