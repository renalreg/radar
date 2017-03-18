from radar.api.serializers.demographics import EthnicitySerializer, NationalitySerializer
from radar.api.views.common import CountryRequestSerializer
from radar.api.views.generics import ListModelView, parse_args
from radar.models import CountryEthnicity, CountryNationality, Ethnicity, Nationality


class EthnicityListView(ListModelView):
    serializer_class = EthnicitySerializer
    model_class = Ethnicity

    def filter_query(self, query):
        query = super(EthnicityListView, self).filter_query(query)
        args = parse_args(CountryRequestSerializer)
        country = args.get('group_country', None)
        query = query.join('countries').filter(CountryEthnicity.country_code == country)
        return query


class NationalityListView(ListModelView):
    serializer_class = NationalitySerializer
    model_class = Nationality

    def filter_query(self, query):
        query = super(NationalityListView, self).filter_query(query)
        args = parse_args(CountryRequestSerializer)
        country = args.get('group_country', None)
        query = query.join('countries').filter(CountryNationality.country_code == country)
        return query


def register_views(app):
    app.add_url_rule('/ethnicities', view_func=EthnicityListView.as_view('ethnicity_list'))
    app.add_url_rule('/nationalities', view_func=NationalityListView.as_view('nationality_list'))
