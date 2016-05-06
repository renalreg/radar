from radar.models.hnf1b import Hnf1bClinicalPicture
from radar.api.serializers.hnf1b import Hnf1bClinicalPictureSerializer
from radar.api.views.common import (
    PatientObjectListView,
    PatientObjectDetailView
)


class Hnf1bClinicalPictureListView(PatientObjectListView):
    serializer_class = Hnf1bClinicalPictureSerializer
    model_class = Hnf1bClinicalPicture


class Hnf1bClinicalPictureDetailView(PatientObjectDetailView):
    serializer_class = Hnf1bClinicalPictureSerializer
    model_class = Hnf1bClinicalPicture


def register_views(app):
    app.add_url_rule('/hnf1b-clinical-pictures', view_func=Hnf1bClinicalPictureListView.as_view('hnf1b_clinical_picture_list'))
    app.add_url_rule('/hnf1b-clinical-pictures/<id>', view_func=Hnf1bClinicalPictureDetailView.as_view('hnf1b_clinical_picture_detail'))
