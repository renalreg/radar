from radar_api.serializers.mpgn import MpgnClinicalPictureSerializer
from radar.models.mpgn import MpgnClinicalPicture
from radar.validation.mpgn import MpgnClinicalPictureValidation
from radar.views.patients import PatientObjectListView, PatientObjectDetailView


class MpgnClinicalPictureListView(PatientObjectListView):
    serializer_class = MpgnClinicalPictureSerializer
    model_class = MpgnClinicalPicture
    validation_class = MpgnClinicalPictureValidation


class MpgnClinicalPictureDetailView(PatientObjectDetailView):
    serializer_class = MpgnClinicalPictureSerializer
    model_class = MpgnClinicalPicture
    validation_class = MpgnClinicalPictureValidation


def register_views(app):
    app.add_url_rule('/mpgn-clinical-pictures', view_func=MpgnClinicalPictureListView.as_view('mpgn_clinical_picture_list'))
    app.add_url_rule('/mpgn-clinical-pictures/<id>', view_func=MpgnClinicalPictureDetailView.as_view('mpgn_clinical_picture_detail'))
