from flask import Flask
from flask_cors import CORS

from radar.api.views.demographics import DemographicsList, DemographicsDetail
from radar.api.views.dialysis import DialysisList, DialysisDetail, DialysisTypeList
from radar.api.views.patients import PatientList, PatientDetail
from radar.api.views.posts import PostList, PostDetail
from radar.api.views.renal_imaging import RenalImagingList, RenalImagingDetail
from radar.api.views.salt_wasting_clinical_features import SaltWastingClinicalFeaturesList, \
    SaltWastingClinicalFeaturesDetail

from radar.lib.database import db


app = Flask(__name__)
app.config.from_object('radar.default_settings')
app.config.from_object('radar.api.default_settings')
app.config.from_envvar('RADAR_SETTINGS')

cors = CORS(app)

db.init_app(app)

app.add_url_rule('/patients', view_func=PatientList.as_view('patient_list'))
app.add_url_rule('/patients/<int:id>', view_func=PatientDetail.as_view('patient_detail'))

app.add_url_rule('/demographics', view_func=DemographicsList.as_view('demographics_list'))
app.add_url_rule('/demographics/<int:id>', view_func=DemographicsDetail.as_view('demographics_detail'))
app.add_url_rule('/dialysis', view_func=DialysisList.as_view('dialysis_list'))
app.add_url_rule('/dialysis/<int:id>', view_func=DialysisDetail.as_view('dialysis_detail'))
app.add_url_rule('/dialysis-types', view_func=DialysisTypeList.as_view('dialysis_type_list'))
app.add_url_rule('/salt-wasting-clinical-features', view_func=SaltWastingClinicalFeaturesList.as_view('salt_wasting_clinical_features_list'))
app.add_url_rule('/salt-wasting-clinical-features/<int:id>', view_func=SaltWastingClinicalFeaturesDetail.as_view('salt_wasting_clinical_features_detail'))
app.add_url_rule('/renal-imaging', view_func=RenalImagingList.as_view('renal_imaging_list'))
app.add_url_rule('/renal-imaging/<int:id>', view_func=RenalImagingDetail.as_view('renal_imaging_detail'))

app.add_url_rule('/posts', view_func=PostList.as_view('post_list'))
app.add_url_rule('/posts/<int:id>', view_func=PostDetail.as_view('post_detail'))

if __name__ == '__main__':
    app.run()
