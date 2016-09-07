import uuid
from functools import wraps

from flask import request, jsonify, Response, abort
from flask.views import MethodView
from sqlalchemy import desc, inspect, Integer
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.dialects import postgresql
from cornflake import fields, serializers
from cornflake.exceptions import ValidationError

from radar.auth.sessions import current_user
from radar.database import db
from radar.exceptions import PermissionDenied, NotFound, BadRequest
from radar.utils import snake_case, camel_case


def parse_args(serializer_class, args=None):
    if args is None:
        args = request.args

    # Remove empty arguments
    args = {k: v for k, v in args.items() if len(v.strip()) > 0}

    # Camel case to snake case
    args = snake_case(args)

    context = {'user': current_user._get_current_object()}

    serializer = serializer_class(data=args, context=context)
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data

    return data


class ApiView(MethodView):
    def dispatch_request(self, *args, **kwargs):
        try:
            return super(ApiView, self).dispatch_request(*args, **kwargs)
        except BadRequest:
            abort(400)
        except PermissionDenied:
            abort(403)
        except NotFound:
            abort(404)
        except ValidationError as e:
            print e.errors
            errors = camel_case(e.errors)
            return jsonify(errors=errors), 422


class PermissionViewMixin(object):
    permission_classes = []

    def check_permissions(self):
        for permission in self.get_permissions():
            if not permission.has_permission(request, current_user):
                print 'Denied by', permission
                raise PermissionDenied()

    def check_object_permissions(self, obj):
        for permission in self.get_permissions():
            if not permission.has_object_permission(request, current_user, obj):
                print 'Denied by', permission
                raise PermissionDenied()

    def get_permission_classes(self):
        return list(self.permission_classes)

    def get_permissions(self):
        return [permission() for permission in self.get_permission_classes()]

    def dispatch_request(self, *args, **kwargs):
        try:
            self.check_permissions()
        except PermissionDenied:
            abort(403)

        return super(PermissionViewMixin, self).dispatch_request(*args, **kwargs)


class SerializerViewMixin(object):
    serializer_class = None

    def get_serializer_class(self):
        return self.serializer_class

    def get_serializer(self, instance=None, data=None, partial=False):
        if data is not None:
            data = snake_case(data)

        context = self.get_context()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(instance=instance, data=data, context=context, partial=partial)
        return serializer

    def get_context(self):
        return {'user': current_user._get_current_object()}


class BaseView(SerializerViewMixin, PermissionViewMixin, ApiView):
    pass


class SortRequestSerializer(serializers.Serializer):
    sort = fields.StringField(required=False)


class PaginationRequestSerializer(serializers.Serializer):
    page = fields.IntegerField(required=False, default=1)
    per_page = fields.IntegerField(required=False)


class PaginationResponseSerializer(serializers.Serializer):
    page = fields.IntegerField()
    per_page = fields.IntegerField()
    count = fields.IntegerField()


class ModelView(SerializerViewMixin, PermissionViewMixin, ApiView):
    sort_fields = {}
    model_class = None

    def filter_query(self, query):
        return query

    def get_sort_args(self):
        args = parse_args(SortRequestSerializer)

        sort = args['sort']

        if sort:
            if sort[0] == '-':
                return sort[1:], True
            else:
                return sort, False
        else:
            return None, False

    def sort_query(self, query):
        sort, reverse = self.get_sort_args()

        if sort is not None:
            sort_fields = self.get_sort_fields()

            if isinstance(sort_fields, dict):
                expression = sort_fields.get(sort)
            elif sort in sort_fields:
                model_class = self.get_model_class()
                expression = getattr(model_class, sort)
            else:
                expression = None

            if expression is not None:
                if reverse:
                    expression = desc(expression)

                query = query.order_by(expression)

        return query

    def paginate_query(self, query):
        args = parse_args(PaginationRequestSerializer)

        page = args['page']
        per_page = args['per_page']

        if per_page is not None:
            if page < 1:
                page = 1

            if per_page < 1:
                per_page = 1

            count = query.count()
            query = query.limit(per_page).offset((page - 1) * per_page)

            pagination = {
                'page': page,
                'per_page': per_page,
                'count': count
            }
        else:
            pagination = None

        return query, pagination

    def get_object_list(self):
        query = self.get_query()
        query = self.filter_query(query)
        query = self.sort_query(query)
        query, pagination = self.paginate_query(query)

        obj_list = query.all()

        return obj_list, pagination

    def get_object(self):
        query = self.get_query()
        query = self.filter_query(query)

        model_class = self.get_model_class()
        id_type = inspect(model_class).columns['id'].type

        obj_id = request.view_args['id']

        if isinstance(id_type, Integer):
            try:
                obj_id = int(obj_id)
            except ValueError:
                raise NotFound()
        elif isinstance(id_type, postgresql.UUID):
            try:
                uuid.UUID(obj_id)
            except ValueError:
                raise NotFound()

        query = query.filter(model_class.id == obj_id)

        try:
            obj = query.one()
        except NoResultFound:
            raise NotFound()

        self.check_object_permissions(obj)

        return obj

    def get_sort_fields(self):
        return self.sort_fields

    def get_model_class(self):
        return self.model_class

    def get_query(self):
        return self.get_model_class().query


class CreateModelViewMixin(object):
    def create(self, *args, **kwargs):
        json = request.get_json()

        if json is None:
            raise BadRequest()

        serializer = self.get_serializer(data=json)
        serializer.is_valid(raise_exception=True)
        obj = serializer.save()

        db.session.add(obj)
        db.session.commit()

        data = serializer.data
        data = camel_case(data)

        return jsonify(data), 200


class ListViewMixin(object):
    def list(self, *args, **kwargs):
        obj_list = self.get_object_list()

        context = self.get_context()
        serializer = self.get_serializer()
        list_serializer = serializers.ListSerializer(obj_list, child=serializer, context=context)

        data = {
            'data': list_serializer.data
        }

        data = camel_case(data)

        return jsonify(data)


class ListModelViewMixin(object):
    def list(self, *args, **kwargs):
        obj_list, pagination = self.get_object_list()

        context = self.get_context()
        serializer = self.get_serializer()
        list_serializer = serializers.ListSerializer(obj_list, child=serializer, context=context)

        data = {
            'data': list_serializer.data
        }

        if pagination:
            pagination_serializer = PaginationResponseSerializer(pagination)
            data['pagination'] = pagination_serializer.data

        data = camel_case(data)

        return jsonify(data)


class RetrieveModelViewMixin(object):
    def retrieve(self, *args, **kwargs):
        obj = self.get_object()
        serializer = self.get_serializer(obj)
        data = serializer.data
        data = camel_case(data)
        return jsonify(data)


class UpdateModelViewMixin(object):
    def update(self, *args, **kwargs):
        json = request.get_json()

        if json is None:
            raise BadRequest()

        partial = request.method == 'PATCH'
        obj = self.get_object()
        serializer = self.get_serializer(obj, data=json, partial=partial)
        serializer.is_valid(raise_exception=True)
        obj = serializer.save()

        db.session.add(obj)
        db.session.commit()

        data = serializer.data
        data = camel_case(data)

        return jsonify(data)


class DestroyModelViewMixin(object):
    def destroy(self, *args, **kwargs):
        obj = self.get_object()
        db.session.delete(obj)
        db.session.commit()
        return Response(status=200)


class RetrieveModelView(RetrieveModelViewMixin, ModelView):
    def get(self, *args, **kwargs):
        return self.retrieve(*args, **kwargs)


class ListView(ListViewMixin, BaseView):
    def get(self, *args, **kwargs):
        return self.list(*args, **kwargs)


class ListModelView(ListModelViewMixin, ModelView):
    def get(self, *args, **kwargs):
        return self.list(*args, **kwargs)


class ListCreateModelView(ListModelViewMixin, CreateModelViewMixin, ModelView):
    def get(self, *args, **kwargs):
        return self.list(*args, **kwargs)

    def post(self, *args, **kwargs):
        return self.create(*args, **kwargs)


class RetrieveUpdateDestroyModelView(RetrieveModelViewMixin, UpdateModelViewMixin, DestroyModelViewMixin, ModelView):
    def get(self, *args, **kwargs):
        return self.retrieve(*args, **kwargs)

    def patch(self, *args, **kwargs):
        return self.update(*args, **kwargs)

    def put(self, *args, **kwargs):
        return self.update(*args, **kwargs)

    def post(self, *args, **kwargs):
        return self.update(*args, **kwargs)

    def delete(self, *args, **kwargs):
        return self.destroy(*args, **kwargs)


class RetrieveUpdateModelView(RetrieveModelViewMixin, UpdateModelViewMixin, ModelView):
    def get(self, *args, **kwargs):
        return self.retrieve(*args, **kwargs)

    def patch(self, *args, **kwargs):
        return self.update(*args, **kwargs)

    def put(self, *args, **kwargs):
        return self.update(*args, **kwargs)

    def post(self, *args, **kwargs):
        return self.update(*args, **kwargs)


class CreateModelView(CreateModelViewMixin, ModelView):
    def post(self, *args, **kwargs):
        return self.create(*args, **kwargs)


class UpdateModelView(UpdateModelViewMixin, ModelView):
    def patch(self, *args, **kwargs):
        return self.update(*args, **kwargs)

    def put(self, *args, **kwargs):
        return self.update(*args, **kwargs)

    def post(self, *args, **kwargs):
        return self.update(*args, **kwargs)


class DestroyModelView(DestroyModelViewMixin, ModelView):
    def delete(self, *args, **kwargs):
        return self.destroy(*args, **kwargs)


def request_json(serializer_class):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            json = request.get_json()

            if json is None:
                raise BadRequest()

            json = snake_case(json)

            context = {}

            if current_user.is_authenticated():
                context['user'] = current_user._get_current_object()

            serializer = serializer_class(data=json, context=context)
            serializer.is_valid(raise_exception=True)
            validated_data = serializer.validated_data

            args = list(args)
            args.append(validated_data)

            return f(*args, **kwargs)

        return wrapper

    return decorator


def response_json(serializer_class):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            response = f(*args, **kwargs)

            context = {}

            if current_user.is_authenticated():
                context['user'] = current_user._get_current_object()

            serializer = serializer_class(response, context=context)
            data = serializer.data
            data = camel_case(data)

            return jsonify(data), 200

        return wrapper

    return decorator
