from flask import Flask
from radar.api.views.demographics import DemographicsList, DemographicsDetail
from radar.api.views.dialysis import DialysisList, DialysisDetail

from radar.lib.database import db


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
