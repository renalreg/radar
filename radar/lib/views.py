from flask import request, jsonify
from flask.views import MethodView
from flask_login import current_user
from sqlalchemy import desc, inspect, or_
from sqlalchemy.orm import aliased
from sqlalchemy.orm.exc import NoResultFound

from radar.lib.database import db
from radar.lib.exceptions import PermissionDenied, NotFound, BadRequest
from radar.lib.patient_search import PatientQueryBuilder
from radar.lib.permissions import PatientDataPermission, FacilityDataPermission, IsAuthenticated, \
    DiseaseGroupDataPermission
from radar.lib.roles import DISEASE_GROUP_VIEW_PATIENT_ROLES, UNIT_VIEW_PATIENT_ROLES
from radar.lib.serializers import ListField, ValidationError, Serializer, IntegerField, StringField
from radar.models import Patient, DiseaseGroupPatient, DiseaseGroup, DiseaseGroupUser, UnitPatient, UnitUser, Unit, \
    Genetics


class ApiView(MethodView):
    permission_classes = []

    def check_permissions(self):
        for permission in self.get_permissions():
            if not permission.has_permission(request, current_user):
                message = getattr(permission, 'message', None)
                raise PermissionDenied(message)

    def check_object_permissions(self, obj):
        for permission in self.get_permissions():
            if not permission.has_object_permission(request, current_user, obj):
                message = getattr(permission, 'message', None)
                raise PermissionDenied(message)

    def get_permission_classes(self):
        return list(self.permission_classes)

    def get_permissions(self):
        return [permission() for permission in self.get_permission_classes()]

    @classmethod
    def error_response(cls, code, detail=None):
        if detail:
            json = jsonify(detail=detail)
        else:
            json = jsonify()

        return json, code

    def dispatch_request(self, *args, **kwargs):
        self.check_permissions()

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

        id = request.view_args['id']
        model_class = self.get_model_class()
        query = query.filter(model_class.id == id)

        try:
            obj = query.one()
        except NoResultFound:
            raise NotFound()

        self.check_object_permissions(obj)

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

    def get_sort_fields(self):
        return self.sort_fields

    def get_model_class(self):
        return self.model_class

    def get_query(self):
        return self.get_model_class().query


class CreateModelMixin(object):
    def create(self, *args, **kwargs):
        serializer = self.get_serializer()

        json = request.get_json()

        if json is None:
            raise BadRequest()

        validated_data = serializer.to_value(json)
        obj = serializer.create(validated_data)

        validator = self.get_validator()

        if validator is not None:
            ctx = {'user': current_user}

            try:
                validator.run_validation(obj, ctx)
            except ValidationError as e:
                errors = serializer.transform_errors(e.detail)
                raise ValidationError(detail=errors)

        db.session.add(obj)
        db.session.commit()
        data = serializer.to_data(obj)
        return jsonify(data), 201


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


class ListModelMixin(object):
    def list(self, *args, **kwargs):
        obj_list, pagination = self.get_object_list()

        serializer = self.get_serializer()
        list_serializer = ListSerializer(serializer)

        response = {'data': obj_list}

        if pagination:
            response['pagination'] = pagination

        data = list_serializer.to_data(response)

        return jsonify(data)


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
            raise BadRequest()

        validated_data = serializer.to_value(json)
        obj = serializer.update(obj, validated_data)

        validator = self.get_validator()

        if validator is not None:
            ctx = {'user': current_user}

            try:
                validator.run_validation(obj, ctx)
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


class RetrieveView(RetrieveModelMixin, GenericApiView):
    def get(self, *args, **kwargs):
        return self.retrieve(*args, **kwargs)


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


class PatientRequestSerializer(Serializer):
    patient_id = IntegerField()


class PatientDataMixin(object):
    def get_permission_classes(self):
        permission_classes = super(PatientDataMixin, self).get_permission_classes()

        if IsAuthenticated not in permission_classes:
            permission_classes.insert(0, IsAuthenticated)

        permission_classes += [PatientDataPermission]

        return permission_classes

    def filter_query(self, query):
        query = super(PatientDataMixin, self).filter_query(query)

        patients_query = PatientQueryBuilder(current_user).build().subquery()
        query = query.join(patients_query)

        serializer = PatientRequestSerializer()
        args = serializer.to_value(request.args)

        if 'patient_id' in args:
            model_class = self.get_model_class()
            query = query.filter(model_class.patient_id == args['patient_id'])

        return query


class FacilityRequestSerializer(Serializer):
    facility_id = IntegerField()


class FacilityDataMixin(object):
    def get_permission_classes(self):
        permission_classes = super(FacilityDataMixin, self).get_permission_classes()

        if IsAuthenticated not in permission_classes:
            permission_classes.insert(0, IsAuthenticated)

        permission_classes += [FacilityDataPermission]

        return permission_classes

    def filter_query(self, query):
        query = super(FacilityDataMixin, self).filter_query(query)

        # Note: if a user can view the patient (see PatientDataMixin.filter_query) they can *view* the patient's data
        # from any facility.

        serializer = FacilityRequestSerializer()
        args = serializer.to_value(request.args)

        # Filter by facility
        if 'facility_id' in args:
            model_class = self.get_model_class()
            query = query.filter(model_class.facility_id == args['facility_id'])

        return query


class DiseaseGroupRequestSerializer(Serializer):
    disease_group_id = IntegerField()


class DiseaseGroupDataMixin(object):
    def get_permission_classes(self):
        permission_classes = super(DiseaseGroupDataMixin, self).get_permission_classes()

        if IsAuthenticated not in permission_classes:
            permission_classes.insert(0, IsAuthenticated)

        permission_classes += [DiseaseGroupDataPermission]

        return permission_classes

    def filter_query(self, query):
        query = super(DiseaseGroupDataMixin, self).filter_query(query)

        # Filter the query based on the user's unit and disease group membership
        # Admins can view all data so don't filter their queries
        if not current_user.is_admin:
            model_class = self.get_model_class()

            # Check if the user has permission through their disease group membership (requires the view patient
            # permission).
            disease_group_sub_query = db.session.query(DiseaseGroupPatient)\
                .join(DiseaseGroupPatient.disease_group)\
                .join(DiseaseGroup.disease_group_users)\
                .filter(
                    DiseaseGroupPatient.patient_id == model_class.patient_id,
                    DiseaseGroupPatient.disease_group_id == model_class.disease_group_id,
                    DiseaseGroupUser.user == current_user,
                    DiseaseGroupUser.role.in_(DISEASE_GROUP_VIEW_PATIENT_ROLES)
                )\
                .exists()

            # Check if the user has permission through their unit membership. If the user has the view patient
            # permission on one of the patient's units they can view all disease group data.
            unit_sub_query = db.session.query(UnitPatient)\
                .join(UnitPatient.unit)\
                .join(Unit.unit_users)\
                .filter(
                    UnitPatient.patient_id == model_class.patient_id,
                    UnitUser.user == current_user,
                    UnitUser.role.in_(UNIT_VIEW_PATIENT_ROLES)
                )\
                .exists()

            # Filter the query to only include rows the user has permission to see
            # Permission is granted through the user's disease group membership and/or unit membership
            query = query.filter(or_(
                disease_group_sub_query,
                unit_sub_query
            ))

        serializer = DiseaseGroupRequestSerializer()
        args = serializer.to_value(request.args)

        # Filter by disease group
        # Note: we don't check permissions here as the query has already been filtered. If the user doesn't belong to
        # the disease group no results will be returned.
        if 'disease_group_id' in args:
            model_class = self.get_model_class()
            query = query.filter(model_class.disease_group_id == args['disease_group_id'])

        return query


class PatientDataList(PatientDataMixin, ListCreateApiView):
    pass


class PatientDataDetail(PatientDataMixin, RetrieveUpdateDestroyAPIView):
    pass
