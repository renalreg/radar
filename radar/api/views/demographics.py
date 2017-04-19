from radar.api.serializers.demographics import EthnicitySerializer, NationalitySerializer
from radar.api.views.common import DemographicsRequestSerializer
from radar.api.views.generics import ListModelView, parse_args

from radar.models import CountryEthnicity, CountryNationality, Ethnicity, Nationality
from radar.models.groups import Group, GROUP_TYPE, GroupPatient, GroupUser


class EthnicityListView(ListModelView):
    serializer_class = EthnicitySerializer
    model_class = Ethnicity

    def filter_query(self, query):
        query = super(EthnicityListView, self).filter_query(query)
        args = parse_args(DemographicsRequestSerializer)
        if args['patient']:
            subquery = (
                Group().query
                       .join((GroupPatient, GroupPatient.group_id == Group.id))
                       .filter(Group.type == GROUP_TYPE.HOSPITAL, GroupPatient.patient_id == args['patient'])
                       .subquery()
            )

        if args['user']:
            context = self.get_context()
            user = context.get('user')
            if user.is_admin:
                return query
            subquery = (
                Group().query
                       .join((GroupUser, GroupUser.group_id == Group.id))
                       .filter(Group.type == GROUP_TYPE.HOSPITAL, GroupUser.user_id == args['user'])
                       .subquery()
            )

        if args['user'] or args['patient']:
            query = (
                query.join(CountryEthnicity)
                     .join(subquery, CountryEthnicity.country_code == subquery.c.country_code)
            )
        return query


class NationalityListView(ListModelView):
    serializer_class = NationalitySerializer
    model_class = Nationality

    def filter_query(self, query):
        query = super(NationalityListView, self).filter_query(query)
        args = parse_args(DemographicsRequestSerializer)
        if args['patient']:
            subquery = (
                Group().query
                       .join((GroupPatient, GroupPatient.group_id == Group.id))
                       .filter(Group.type == GROUP_TYPE.HOSPITAL, GroupPatient.patient_id == args['patient'])
                       .subquery()
            )

        if args['user']:
            context = self.get_context()
            user = context.get('user')
            if user.is_admin:
                return query
            subquery = (
                Group().query
                       .join((GroupUser, GroupUser.group_id == Group.id))
                       .filter(Group.type == GROUP_TYPE.HOSPITAL, GroupUser.user_id == args['user'])
                       .subquery()
            )

        if args['user'] or args['patient']:
            query = (
                query.join(CountryNationality)
                     .join(subquery, CountryNationality.country_code == subquery.c.country_code)
            )
        return query


def register_views(app):
    app.add_url_rule('/ethnicities', view_func=EthnicityListView.as_view('ethnicity_list'))
    app.add_url_rule('/nationalities', view_func=NationalityListView.as_view('nationality_list'))
