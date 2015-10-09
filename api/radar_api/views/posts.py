from radar_api.serializers.posts import PostSerializer
from radar.validation.posts import PostValidation
from radar.views.core import ListCreateModelView, RetrieveUpdateDestroyModelView
from radar.models import Post


class PostListView(ListCreateModelView):
    serializer_class = PostSerializer
    model_class = Post
    validation_class = PostValidation
    sort_fields = ('id', 'title', 'published_date')


class PostDetailView(RetrieveUpdateDestroyModelView):
    serializer_class = PostSerializer
    model_class = Post
    validation_class = PostValidation
