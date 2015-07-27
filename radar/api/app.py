from flask import Flask
from radar.api.views.demographics import DemographicsList, DemographicsDetail
from radar.api.views.dialysis import DialysisList, DialysisDetail
from radar.api.views.posts import PostList, PostDetail
from radar.api.views.renal_imaging import RenalImagingList, RenalImagingDetail
from radar.api.views.salt_wasting_clinical_features import SaltWastingClinicalFeaturesList, \
    SaltWastingClinicalFeaturesDetail

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
app.add_url_rule('/api/salt-wasting-clinical-features/', view_func=SaltWastingClinicalFeaturesList.as_view('salt_wasting_clinical_features_list'))
app.add_url_rule('/api/salt-wasting-clinical-features/<int:id>/', view_func=SaltWastingClinicalFeaturesDetail.as_view('salt_wasting_clinical_features_detail'))
app.add_url_rule('/api/renal-imaging/', view_func=RenalImagingList.as_view('renal_imaging_list'))
app.add_url_rule('/api/renal-imaging/<int:id>/', view_func=RenalImagingDetail.as_view('renal_imaging_detail'))
app.add_url_rule('/api/posts/', view_func=PostList.as_view('post_list'))
app.add_url_rule('/api/posts/<int:id>/', view_func=PostDetail.as_view('post_detail'))

if __name__ == '__main__':
    app.run()
