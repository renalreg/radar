from flask import Flask, abort
from flask_cors import CORS
from flask_login import LoginManager
from itsdangerous import TimestampSigner, BadSignature

from radar.api.views.demographics import DemographicsList, DemographicsDetail
from radar.api.views.dialysis import DialysisList, DialysisDetail, DialysisTypeList
from radar.api.views.disease_groups import DiseaseGroupList
from radar.api.views.facilities import FacilityList, FacilityDetail
from radar.api.views.patients import PatientList, PatientDetail
from radar.api.views.posts import PostList, PostDetail
from radar.api.views.renal_imaging import RenalImagingList, RenalImagingDetail
from radar.api.views.salt_wasting_clinical_features import SaltWastingClinicalFeaturesList, \
    SaltWastingClinicalFeaturesDetail
from radar.api.views.users import UserDetail, UserList
from radar.api.views.login import Login

from radar.lib.database import db
from radar.models import User


app = Flask(__name__)
app.config.from_object('radar.default_settings')
app.config.from_object('radar.api.default_settings')
app.config.from_envvar('RADAR_SETTINGS')

cors = CORS(app)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.header_loader
def load_user_from_header(header):
    # TODO
    s = TimestampSigner('SECRET')

    try:
        user_id = int(s.unsign(header, max_age=3600))
    except BadSignature:
        abort(401)

    return User.query.filter(User.id == user_id).first()

db.init_app(app)

app.add_url_rule('/login', view_func=Login.as_view('login'))

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

app.add_url_rule('/users', view_func=UserList.as_view('user_list'))
app.add_url_rule('/users/<int:id>', view_func=UserDetail.as_view('user_detail'))

app.add_url_rule('/facilities', view_func=FacilityList.as_view('facility_list'))
app.add_url_rule('/facilities/<int:id>', view_func=FacilityDetail.as_view('facility_detail'))

app.add_url_rule('/disease-groups', view_func=DiseaseGroupList.as_view('disease_group_list'))

app.add_url_rule('/posts', view_func=PostList.as_view('post_list'))
app.add_url_rule('/posts/<int:id>', view_func=PostDetail.as_view('post_detail'))

if __name__ == '__main__':
    app.run()
