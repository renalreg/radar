from radar.models.alport import AlportClinicalPicture, DEAFNESS_OPTIONS
from radar.serializers.alport import AlportClinicalPictureSerializer
from radar.views.common import (
    PatientObjectListView,
    PatientObjectDetailView,
    IntegerLookupListView
)


class AlportClinicalPictureListView(PatientObjectListView):
    serializer_class = AlportClinicalPictureSerializer
    model_class = AlportClinicalPicture


class AlportClinicalPictureDetailView(PatientObjectDetailView):
    serializer_class = AlportClinicalPictureSerializer
    model_class = AlportClinicalPicture


class AlportDeafnessOptionListView(IntegerLookupListView):
    items = DEAFNESS_OPTIONS


def register_views(app):
    app.add_url_rule('/alport-clinical-pictures', view_func=AlportClinicalPictureListView.as_view('alport_clinical_picture_list'))
    app.add_url_rule('/alport-clinical-pictures/<id>', view_func=AlportClinicalPictureDetailView.as_view('alport_clinical_picture_detail'))
    app.add_url_rule('/alport-deafness-options', view_func=AlportDeafnessOptionListView.as_view('alport_deafness_option_list'))
