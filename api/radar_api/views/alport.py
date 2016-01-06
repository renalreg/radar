from radar_api.serializers.alport import AlportClinicalPictureSerializer
from radar.models.alport import AlportClinicalPicture, DEAFNESS_OPTIONS
from radar.validation.alport import AlportClinicalPictureValidation
from radar.views.patients import PatientObjectListView, PatientObjectDetailView
from radar.views.codes import CodedIntegerListView


class AlportClinicalPictureListView(PatientObjectListView):
    serializer_class = AlportClinicalPictureSerializer
    model_class = AlportClinicalPicture
    validation_class = AlportClinicalPictureValidation


class AlportClinicalPictureDetailView(PatientObjectDetailView):
    serializer_class = AlportClinicalPictureSerializer
    model_class = AlportClinicalPicture
    validation_class = AlportClinicalPictureValidation


class AlportDeafnessOptionListView(CodedIntegerListView):
    items = DEAFNESS_OPTIONS


def register_views(app):
    app.add_url_rule('/alport-clinical-pictures', view_func=AlportClinicalPictureListView.as_view('alport_clinical_picture_list'))
    app.add_url_rule('/alport-clinical-pictures/<id>', view_func=AlportClinicalPictureDetailView.as_view('alport_clinical_picture_detail'))
    app.add_url_rule('/alport-deafness-options', view_func=AlportDeafnessOptionListView.as_view('alport_deafness_option_list'))
