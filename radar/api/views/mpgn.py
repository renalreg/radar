from radar.api.serializers.mpgn import MpgnClinicalPictureSerializer
from radar.api.views.common import PatientObjectListView, PatientObjectDetailView
from radar.models.mpgn import MpgnClinicalPicture


class MpgnClinicalPictureListView(PatientObjectListView):
    serializer_class = MpgnClinicalPictureSerializer
    model_class = MpgnClinicalPicture


class MpgnClinicalPictureDetailView(PatientObjectDetailView):
    serializer_class = MpgnClinicalPictureSerializer
    model_class = MpgnClinicalPicture


def register_views(app):
    app.add_url_rule('/mpgn-clinical-pictures', view_func=MpgnClinicalPictureListView.as_view('mpgn_clinical_picture_list'))
    app.add_url_rule('/mpgn-clinical-pictures/<id>', view_func=MpgnClinicalPictureDetailView.as_view('mpgn_clinical_picture_detail'))
