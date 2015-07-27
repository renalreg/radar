from flask import Flask

from radar.lib.database import db
from radar.lib.serializers import ModelSerializer, MetaSerializerMixin, FacilitySerializerMixin
from radar.lib.views import FacilityDataMixin, PatientDataList, PatientDataDetail
from radar.models import PatientDemographics, Dialysis


class DemographicsSerializer(MetaSerializerMixin, FacilitySerializerMixin, ModelSerializer):
    class Meta:
        model = PatientDemographics


class DemographicsList(FacilityDataMixin, PatientDataList):
    serializer_class = DemographicsSerializer

    def get_query(self):
        return PatientDemographics.query


class DemographicsDetail(FacilityDataMixin, PatientDataDetail):
    serializer_class = DemographicsSerializer

    def get_query(self):
        return PatientDemographics.query


class DialysisSerializer(MetaSerializerMixin, FacilitySerializerMixin, ModelSerializer):
    class Meta:
        model = Dialysis


class DialysisList(FacilityDataMixin, PatientDataList):
    serializer_class = DialysisSerializer

    def get_query(self):
        return Dialysis.query


class DialysisDetail(FacilityDataMixin, PatientDataDetail):
    serializer_class = DialysisSerializer

    def get_query(self):
        return Dialysis.query


app = Flask(__name__)
app.config.from_object('radar.default_settings')
app.config.from_object('radar.api.default_settings')
app.config.from_envvar('RADAR_SETTINGS')

db.init_app(app)

app.add_url_rule('/api/demographics/', view_func=DemographicsList.as_view('demographics_list'))
app.add_url_rule('/api/demographics/<int:id>/', view_func=DemographicsDetail.as_view('demographics_detail'))
app.add_url_rule('/api/dialysis/', view_func=DialysisList.as_view('dialysis_list'))
app.add_url_rule('/api/dialysis/<int:id>/', view_func=DialysisDetail.as_view('dialysis_detail'))

if __name__ == '__main__':
    app.run()
