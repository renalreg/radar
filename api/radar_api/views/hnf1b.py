from radar_api.serializers.ins import Hnf1bClinicalPictureSerializer
from radar.models.hnf1b import Hnf1bClinicalPicture, TYPES_OF_DIALYSIS
from radar.validation.hnf1b import Hnf1bClinicalPictureValidation
from radar.views.patients import PatientObjectListView, PatientObjectDetailView
from radar.views.codes import CodedStringListView


class Hnf1bClinicalPictureListView(PatientObjectListView):
    serializer_class = Hnf1bClinicalPictureSerializer
    model_class = Hnf1bClinicalPicture
    validation_class = Hnf1bClinicalPictureValidation


class Hnf1bClinicalPictureDetailView(PatientObjectDetailView):
    serializer_class = Hnf1bClinicalPictureSerializer
    model_class = Hnf1bClinicalPicture
    validation_class = Hnf1bClinicalPictureValidation


class Hnf1bDialysisTypeListView(CodedStringListView):
    items = TYPES_OF_DIALYSIS


def register_views(app):
    app.add_url_rule('/hnf1b-clinical-pictures', view_func=Hnf1bClinicalPictureListView.as_view('hnf1b_clinical_picture_list'))
    app.add_url_rule('/hnf1b-clinical-pictures/<id>', view_func=Hnf1bClinicalPictureDetailView.as_view('hnf1b_clinical_picture_detail'))
    app.add_url_rule('/hnf1b-dialysis-types', view_func=Hnf1bDialysisTypeListView.as_view('hnf1b_dialysis_type_list'))
