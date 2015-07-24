from flask import Flask, jsonify, abort, request
from flask.views import MethodView
from cerberus import Validator

from radar.lib.database import db
from radar.lib.serializers import Serializer, IntegerSerializer, StringSerializer
from radar.lib.views import ListCreateApiView
from radar.models import PatientDemographics


app = Flask(__name__)
app.config.from_object('radar.default_settings')
app.config.from_object('radar.api.default_settings')
app.config.from_envvar('RADAR_SETTINGS')

db.init_app(app)


class DemographicsSerializer(Serializer):
    id = IntegerSerializer()
    first_name = StringSerializer()
    last_name = StringSerializer()


class DemographicsList(ListCreateApiView):
    serializer_class = DemographicsSerializer

    def get_queryset(self):
        return PatientDemographics.query.all()


app.add_url_rule('/api/demographics', view_func=DemographicsList.as_view('demographics_list'))

if __name__ == '__main__':
    app.run()
