from os import abort
from flask import request, jsonify
from flask.views import MethodView
from radar.lib.serializers import ListSerializer


class ApiView(MethodView):
    permission_classes = []

    def check_permissions(self):
        for permission in self.get_permissions():
            if not permission.has_permission():
                # TODO
                pass

    def check_object_permission(self, obj):
        for permission in self.get_permissions():
            if not permission.has_object_permission(obj):
                # TODO
                pass

    def get_permissions(self):
        return [permission() for permission in self.permission_classes]


class GenericApiView(ApiView):
    def get_object(self):
        pass

    def get_queryset(self):
        raise NotImplementedError()

    def get_serializer(self):
        return self.get_serializer_class()()

    def get_serializer_class(self):
        return self.serializer_class


class CreateModelMixin(object):
    def create(self, *args, **kwargs):
        pass


class ListModelMixin(object):
    def list(self, *args, **kwargs):
        items = self.get_queryset()
        serializer = ListSerializer(self.get_serializer())
        data = serializer.to_data(items)
        return jsonify(data=data)


class RetrieveModelMixin(object):
    def retrieve(self, *args, **kwargs):
        pass


class UpdateModelMixin(object):
    def update(self, *args, **kwargs):
        pass


class DestroyModelMixin(object):
    def destroy(self, *args, **kwargs):
        pass


class ListCreateApiView(ListModelMixin, CreateModelMixin, GenericApiView):
    def get(self, *args, **kwargs):
        return self.list(*args, **kwargs)

    def post(self, *args, **kwargs):
        return self.create(*args, **kwargs)


class RetrieveUpdateDestroyAPIView(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericApiView):
    def get(self, *args, **kwargs):
        return self.retrieve(*args, **kwargs)

    def put(self, *args, **kwargs):
        return self.update(*args, **kwargs)

    def delete(self, *args, **kwargs):
        return self.delete(*args, **kwargs)
