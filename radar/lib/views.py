from flask import request, jsonify
from flask.views import MethodView
from sqlalchemy.orm.exc import NoResultFound

from radar.lib.database import db
from radar.lib.exceptions import PermissionDenied, NotFound, BadRequest
from radar.lib.permissions import PatientDataPermission, FacilityDataPermission

from radar.lib.serializers import ListField, ValidationError


class ApiView(MethodView):
    permission_classes = []

    def check_permissions(self):
        for permission in self.get_permissions():
            if not permission.has_permission():
                message = getattr(permission, 'message', None)
                raise PermissionDenied(message)

    def check_object_permission(self, obj):
        for permission in self.get_permissions():
            if not permission.has_object_permission(obj):
                message = getattr(permission, 'message', None)
                raise PermissionDenied(message)

    def get_permissions(self):
        return [permission() for permission in self.permission_classes]

    @classmethod
    def error_response(cls, code, detail=None):
        if detail:
            json = jsonify(detail=detail)
        else:
            json = jsonify()

        return json, code

    def dispatch_request(self, *args, **kwargs):
        try:
            return super(ApiView, self).dispatch_request(*args, **kwargs)
        except BadRequest as e:
            return self.error_response(400, e.detail)
        except PermissionDenied as e:
            return self.error_response(403, e.detail)
        except NotFound as e:
            return self.error_response(404, e.detail)
        except ValidationError as e:
            return jsonify(errors=e.detail), 422


class GenericApiView(ApiView):
    serializer_class = None
    validator_class = None

    def get_query(self):
        raise NotImplementedError()

    def filter_query(self, query):
        return query

    def get_object_list(self):
        query = self.get_query()
        query = self.filter_query(query)

        obj_list = query.all()

        return obj_list

    def get_object(self):
        query = self.get_query()
        query = self.filter_query(query)

        id = request.view_args['id']
        query = query.filter_by(id=id)

        try:
            obj = query.one()
        except NoResultFound:
            raise NotFound()

        self.check_object_permission(obj)

        return obj

    def get_serializer(self):
        return self.get_serializer_class()()

    def get_serializer_class(self):
        return self.serializer_class

    def get_validator_class(self):
        return self.validator_class

    def get_validator(self):
        validator_class = self.get_validator_class()

        if validator_class is None:
            return None
        else:
            return validator_class()


class CreateModelMixin(object):
    def create(self, *args, **kwargs):
        serializer = self.get_serializer()

        json = request.get_json()

        if json is None:
            raise BadRequest('Expected JSON.')

        validated_data = serializer.to_value(json)
        obj = serializer.create(validated_data)

        validator = self.get_validator()

        if validator is not None:
            try:
                validator.run_validation(obj)
            except ValidationError as e:
                errors = serializer.transform_errors(e.detail)
                raise ValidationError(detail=errors)

        db.session.add(obj)
        db.session.commit()
        data = serializer.to_data(obj)
        return jsonify(data), 201


class ListModelMixin(object):
    def list(self, *args, **kwargs):
        obj_list = self.get_object_list()
        serializer = ListField(self.get_serializer())
        data = serializer.to_data(obj_list)
        return jsonify(data=data)


class RetrieveModelMixin(object):
    def retrieve(self, *args, **kwargs):
        obj = self.get_object()
        serializer = self.get_serializer()
        data = serializer.to_data(obj)
        return jsonify(data)


class UpdateModelMixin(object):
    def update(self, *args, **kwargs):
        obj = self.get_object()
        serializer = self.get_serializer()

        json = request.get_json()

        if json is None:
            raise BadRequest('Expected JSON.')

        validated_data = serializer.to_value(json)
        obj = serializer.update(obj, validated_data)

        validator = self.get_validator()

        if validator is not None:
            try:
                validator.run_validation(obj)
            except ValidationError as e:
                errors = serializer.transform_errors(e.detail)
                raise ValidationError(detail=errors)

        db.session.commit()
        data = serializer.to_data(obj)
        return jsonify(data)


class DestroyModelMixin(object):
    def destroy(self, *args, **kwargs):
        obj = self.get_object()
        db.session.delete(obj)
        db.session.commit()
        return '', 204


class ListView(ListModelMixin, GenericApiView):
    def get(self, *args, **kwargs):
        return self.list(*args, **kwargs)


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

    def post(self, *args, **kwargs):
        return self.update(*args, **kwargs)

    def delete(self, *args, **kwargs):
        return self.destroy(*args, **kwargs)


class PatientDataMixin(object):
    def get_permission_classes(self):
        permission_classes = super(PatientDataMixin, self).get_permission_classes()
        permission_classes += [PatientDataPermission]
        return permission_classes

    def filter_query(self, query):
        query = super(PatientDataMixin, self).filter_query(query)

        patient_id = request.args.get('patientId')

        if patient_id is not None:
            try:
                patient_id = int(patient_id)
            except ValueError:
                raise BadRequest('patientId must be an integer.')

            # TODO permissions
            query = query.filter_by(patient_id=patient_id)
        else:
            # TODO filter
            pass

        return query


class FacilityDataMixin(object):
    def get_permission_classes(self):
        permission_classes = super(FacilityDataMixin, self).get_permission_classes()
        permission_classes += [FacilityDataPermission]
        return permission_classes

    def filter_query(self, query):
        query = super(FacilityDataMixin, self).filter_query(query)

        facility_id = request.args.get('facilityId')

        if facility_id is not None:
            try:
                facility_id = int(facility_id)
            except ValueError:
                raise BadRequest('facilityId must be an integer.')

            # TODO permissions
            query = query.filter_by(facility_id=facility_id)
        else:
            # TODO filter
            pass

        return query


class PatientDataList(PatientDataMixin, ListCreateApiView):
    pass


class PatientDataDetail(PatientDataMixin, RetrieveUpdateDestroyAPIView):
    pass
