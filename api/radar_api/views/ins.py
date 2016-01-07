from radar_api.serializers.ins import InsClinicalPictureSerializer, InsRelapseSerializer
from radar.models.ins import InsClinicalPicture, InsRelapse, KIDNEY_TYPES, REMISSION_TYPES
from radar.validation.ins import InsClinicalPictureValidation, InsRelapseValidation
from radar.views.patients import PatientObjectListView, PatientObjectDetailView
from radar.views.codes import CodedStringListView


class InsClinicalPictureListView(PatientObjectListView):
    serializer_class = InsClinicalPictureSerializer
    model_class = InsClinicalPicture
    validation_class = InsClinicalPictureValidation


class InsClinicalPictureDetailView(PatientObjectDetailView):
    serializer_class = InsClinicalPictureSerializer
    model_class = InsClinicalPicture
    validation_class = InsClinicalPictureValidation


class InsRelapseListView(PatientObjectListView):
    serializer_class = InsRelapseSerializer
    model_class = InsRelapse
    validation_class = InsRelapseValidation


class InsRelapseDetailView(PatientObjectDetailView):
    serializer_class = InsRelapseSerializer
    model_class = InsRelapse
    validation_class = InsRelapseValidation


class InsKidneyTypeListView(CodedStringListView):
    items = KIDNEY_TYPES


class InsRemissionTypeListView(CodedStringListView):
    items = REMISSION_TYPES


def register_views(app):
    app.add_url_rule('/ins-clinical-pictures', view_func=InsClinicalPictureListView.as_view('ins_clinical_picture_list'))
    app.add_url_rule('/ins-clinical-pictures/<id>', view_func=InsClinicalPictureDetailView.as_view('ins_clinical_picture_detail'))
    app.add_url_rule('/ins-relapses', view_func=InsRelapseListView.as_view('ins_relapse_list'))
    app.add_url_rule('/ins-relapses/<id>', view_func=InsRelapseDetailView.as_view('ins_relapse_detail'))
    app.add_url_rule('/ins-kidney-types', view_func=InsKidneyTypeListView.as_view('ins_kidney_type_list'))
    app.add_url_rule('/ins-remission-types', view_func=InsRemissionTypeListView.as_view('ins_remission_type_list'))
