from functools import wraps
import uuid

from flask import request, jsonify
from flask.views import MethodView
from sqlalchemy import desc, inspect, Integer
from sqlalchemy.orm.exc import NoResultFound
from flask import abort
from sqlalchemy.dialects import postgresql

from radar.database import db
from radar.exceptions import PermissionDenied, NotFound, BadRequest
from radar.serializers.core import Serializer
from radar.serializers.fields import StringField, IntegerField, ListField
from radar.validation.core import ValidationError
from radar.auth.sessions import current_user


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
            return jsonify(errors=e.errors), 422


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

    def get_serializer(self):
        return self.get_serializer_class()()

    def get_serializer_class(self):
        return self.serializer_class


class ValidationViewMixin(object):
    validation_class = None

    def get_validation_class(self):
        return self.validation_class

    def get_validation(self):
        validation_class = self.get_validation_class()

        if validation_class is None:
            return None
        else:
            return validation_class()

    def get_context(self, deserialized_data):
        return {'user': current_user}


class BaseView(SerializerViewMixin, ValidationViewMixin, PermissionViewMixin, ApiView):
    pass


class ModelView(SerializerViewMixin, ValidationViewMixin, PermissionViewMixin, ApiView):
    sort_fields = {}
    model_class = None

    def filter_query(self, query):
        return query

    def get_sort_args(self):
        sort_serializer = SortRequestSerializer()
        sort_args = sort_serializer.to_value(request.args)
        sort = sort_args.get('sort')

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
        pagination_serializer = PaginationRequestSerializer()
        pagination_args = pagination_serializer.to_value(request.args)

        per_page = pagination_args.get('per_page')

        if per_page is not None:
            page = pagination_args.get('page', 1)

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
        serializer = self.get_serializer()

        json = request.get_json()

        if json is None:
            raise BadRequest()

        deserialized_data = serializer.to_value(json)

        validation = self.get_validation()

        if validation is None:
            obj = serializer.create()
            obj = serializer.update(obj, deserialized_data)
        else:
            ctx = self.get_context(deserialized_data)
            obj = serializer.create()

            with db.session.no_autoflush:
                try:
                    validation.before_update(ctx, obj)
                    old_obj = validation.clone(obj)
                    obj = serializer.update(obj, deserialized_data)
                    validation.after_update(ctx, old_obj, obj)
                except ValidationError as e:
                    print e.errors
                    errors = serializer.transform_errors(e.errors)
                    raise ValidationError(errors)

        db.session.add(obj)
        db.session.commit()
        data = serializer.to_data(obj)
        return jsonify(data), 200


class SortRequestSerializer(Serializer):
    sort = StringField()


class PaginationRequestSerializer(Serializer):
    page = IntegerField()
    per_page = IntegerField()


class PaginationResponseSerializer(Serializer):
    page = IntegerField()
    per_page = IntegerField()
    count = IntegerField()


class ListSerializer(Serializer):
    pagination = PaginationResponseSerializer()

    def __init__(self, serializer, *args, **kwargs):
        super(ListSerializer, self).__init__(*args, **kwargs)
        self.serializer = serializer

    def get_fields(self):
        fields = super(ListSerializer, self).get_fields()

        data_field = ListField(self.serializer)
        data_field.bind('data')
        fields['data'] = data_field

        return fields


class ListViewMixin(object):
    def list(self, *args, **kwargs):
        obj_list = self.get_object_list()

        serializer = self.get_serializer()
        list_serializer = ListSerializer(serializer)
        data = list_serializer.to_data({'data': obj_list})

        return jsonify(data)


class ListModelViewMixin(object):
    def list(self, *args, **kwargs):
        obj_list, pagination = self.get_object_list()

        serializer = self.get_serializer()
        list_serializer = ListSerializer(serializer)

        response = {'data': obj_list}

        if pagination:
            response['pagination'] = pagination

        data = list_serializer.to_data(response)

        return jsonify(data)


class RetrieveModelViewMixin(object):
    def retrieve(self, *args, **kwargs):
        obj = self.get_object()
        serializer = self.get_serializer()
        data = serializer.to_data(obj)
        return jsonify(data)


class UpdateModelViewMixin(object):
    def update(self, *args, **kwargs):
        obj = self.get_object()
        serializer = self.get_serializer()

        json = request.get_json()

        if json is None:
            raise BadRequest()

        deserialized_data = serializer.to_value(json)

        validation = self.get_validation()

        if validation is None:
            obj = serializer.update(obj, deserialized_data)
        else:
            ctx = self.get_context(deserialized_data)

            with db.session.no_autoflush:
                try:
                    validation.before_update(ctx, obj)
                    old_obj = validation.clone(obj)
                    obj = serializer.update(obj, deserialized_data)
                    validation.after_update(ctx, old_obj, obj)
                except ValidationError as e:
                    errors = serializer.transform_errors(e.errors)
                    raise ValidationError(errors)

        db.session.commit()
        data = serializer.to_data(obj)
        return jsonify(data)


class DestroyModelViewMixin(object):
    def destroy(self, *args, **kwargs):
        obj = self.get_object()
        db.session.delete(obj)
        db.session.commit()
        return '', 200


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

    def put(self, *args, **kwargs):
        return self.update(*args, **kwargs)

    def post(self, *args, **kwargs):
        return self.update(*args, **kwargs)

    def delete(self, *args, **kwargs):
        return self.destroy(*args, **kwargs)


class RetrieveUpdateModelView(RetrieveModelViewMixin, UpdateModelViewMixin, ModelView):
    def get(self, *args, **kwargs):
        return self.retrieve(*args, **kwargs)

    def put(self, *args, **kwargs):
        return self.update(*args, **kwargs)

    def post(self, *args, **kwargs):
        return self.update(*args, **kwargs)


class CreateModelView(CreateModelViewMixin, ModelView):
    def post(self, *args, **kwargs):
        return self.create(*args, **kwargs)


class UpdateModelView(UpdateModelViewMixin, ModelView):
    def put(self, *args, **kwargs):
        return self.update(*args, **kwargs)

    def post(self, *args, **kwargs):
        return self.update(*args, **kwargs)


class DestroyModelView(DestroyModelViewMixin, ModelView):
    def delete(self, *args, **kwargs):
        return self.destroy(*args, **kwargs)


def request_json(serializer_class, validation_class=None):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            json = request.get_json()

            if json is None:
                raise BadRequest()

            serializer = serializer_class()
            data = serializer.to_value(json)

            if validation_class is not None:
                validation = validation_class()

                ctx = {}

                if current_user.is_authenticated():
                    ctx['user'] = current_user

                try:
                    data = validation.after_update(ctx, {}, data)
                except ValidationError as e:
                    errors = serializer.transform_errors(e.errors)
                    raise ValidationError(errors)

            args = list(args)
            args.append(data)

            return f(*args, **kwargs)

        return wrapper

    return decorator


def response_json(serializer_class):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            response = f(*args, **kwargs)
            serializer = serializer_class()
            data = serializer.to_data(response)
            return jsonify(data), 200

        return wrapper

    return decorator
