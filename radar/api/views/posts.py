from radar.api.permissions import AdminPermission
from radar.api.serializers.posts import PostAuthorSerializer, PostSerializer
from radar.api.views.generics import (
    CreateModelView,
    DestroyModelView,
    ListModelView,
    RetrieveModelView,
    UpdateModelView,
)
from radar.models.posts import Post


class PostListView(ListModelView):
    serializer_class = PostSerializer
    model_class = Post
    sort_fields = ("id", "title", "published_date")


class PostCreateView(CreateModelView):
    serializer_class = PostAuthorSerializer
    permission_classes = [AdminPermission]


class PostRetrieveView(RetrieveModelView):
    serializer_class = PostSerializer
    model_class = Post


class PostUpdateView(UpdateModelView):
    serializer_class = PostSerializer
    model_class = Post
    permission_classes = [AdminPermission]


class PostDestroyView(DestroyModelView):
    model_class = Post
    permission_classes = [AdminPermission]


def register_views(app):
    app.add_public_endpoint("post_list")
    app.add_public_endpoint("post_retrieve")

    app.add_url_rule("/posts", view_func=PostListView.as_view("post_list"))
    app.add_url_rule("/posts", view_func=PostCreateView.as_view("post_create"))
    app.add_url_rule(
        "/posts/<int:id>", view_func=PostRetrieveView.as_view("post_retrieve")
    )
    app.add_url_rule("/posts/<int:id>", view_func=PostUpdateView.as_view("post_update"))
    app.add_url_rule(
        "/posts/<int:id>", view_func=PostDestroyView.as_view("post_destroy")
    )
