from radar.api.serializers.ins import InsClinicalPictureSerializer, InsRelapseSerializer
from radar.api.views.common import (
    PatientObjectDetailView,
    PatientObjectListView,
    StringLookupListView,
)
from radar.models.ins import DIPSTICK_TYPES, InsClinicalPicture, InsRelapse, KIDNEY_TYPES, REMISSION_TYPES


class InsClinicalPictureListView(PatientObjectListView):
    serializer_class = InsClinicalPictureSerializer
    model_class = InsClinicalPicture


class InsClinicalPictureDetailView(PatientObjectDetailView):
    serializer_class = InsClinicalPictureSerializer
    model_class = InsClinicalPicture


class InsRelapseListView(PatientObjectListView):
    serializer_class = InsRelapseSerializer
    model_class = InsRelapse


class InsRelapseDetailView(PatientObjectDetailView):
    serializer_class = InsRelapseSerializer
    model_class = InsRelapse


class InsKidneyTypeListView(StringLookupListView):
    items = KIDNEY_TYPES


class InsRemissionTypeListView(StringLookupListView):
    items = REMISSION_TYPES


class InsDipstickListView(StringLookupListView):
    items = DIPSTICK_TYPES


def register_views(app):
    app.add_url_rule(
        '/ins-clinical-pictures',
        view_func=InsClinicalPictureListView.as_view('ins_clinical_picture_list'))
    app.add_url_rule(
        '/ins-clinical-pictures/<id>',
        view_func=InsClinicalPictureDetailView.as_view('ins_clinical_picture_detail'))
    app.add_url_rule('/ins-relapses', view_func=InsRelapseListView.as_view('ins_relapse_list'))
    app.add_url_rule('/ins-relapses/<id>', view_func=InsRelapseDetailView.as_view('ins_relapse_detail'))
    app.add_url_rule('/ins-kidney-types', view_func=InsKidneyTypeListView.as_view('ins_kidney_type_list'))
    app.add_url_rule(
        '/ins-remission-types',
        view_func=InsRemissionTypeListView.as_view('ins_remission_type_list'))
    app.add_url_rule('/ins-dipstick-options', view_func=InsDipstickListView.as_view('ins_dipstick_options'))
