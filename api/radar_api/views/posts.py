from radar_api.serializers.posts import PostSerializer
from radar.validation.posts import PostValidation
from radar.views.core import ListModelView, CreateModelView, RetrieveModelView, \
    UpdateModelView, DestroyModelView

from radar.models import Post


class PostListView(ListModelView):
    serializer_class = PostSerializer
    model_class = Post
    sort_fields = ('id', 'title', 'published_date')


class PostCreateView(CreateModelView):
    serializer_class = PostSerializer
    validation_class = PostValidation


class PostRetrieveView(RetrieveModelView):
    serializer_class = PostSerializer
    model_class = Post


class PostUpdateView(UpdateModelView):
    serializer_class = PostSerializer
    model_class = Post
    validation_class = PostValidation


class PostDestroyView(DestroyModelView):
    model_class = Post


def register_views(app):
    app.add_public_endpoint('post_list')
    app.add_public_endpoint('post_retrieve')

    app.add_url_rule('/posts', view_func=PostListView.as_view('post_list'))
    app.add_url_rule('/posts', view_func=PostCreateView.as_view('post_create'))
    app.add_url_rule('/posts/<int:id>', view_func=PostRetrieveView.as_view('post_retrieve'))
    app.add_url_rule('/posts/<int:id>', view_func=PostUpdateView.as_view('post_update'))
    app.add_url_rule('/posts/<int:id>', view_func=PostDestroyView.as_view('post_destroy'))
