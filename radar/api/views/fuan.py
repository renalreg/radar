from radar.api.serializers.fuan import FuanClinicalPictureSerializer
from radar.api.views.common import (
    IntegerLookupListView,
    PatientObjectDetailView,
    PatientObjectListView,
    StringLookupListView,
)
from radar.models.fuan import FuanClinicalPicture, RELATIVES, THP_RESULTS


class FuanClinicalPictureListView(PatientObjectListView):
    serializer_class = FuanClinicalPictureSerializer
    model_class = FuanClinicalPicture


class FuanClinicalPictureDetailView(PatientObjectDetailView):
    serializer_class = FuanClinicalPictureSerializer
    model_class = FuanClinicalPicture


class FuanRelativeListView(IntegerLookupListView):
    items = RELATIVES


class FuanTHPResultListView(StringLookupListView):
    items = THP_RESULTS


def register_views(app):
    app.add_url_rule(
        '/fuan-clinical-pictures',
        view_func=FuanClinicalPictureListView.as_view('fuan_clinical_picture_list')
    )
    app.add_url_rule(
        '/fuan-clinical-pictures/<id>',
        view_func=FuanClinicalPictureDetailView.as_view('fuan_clinical_picture_detail')
    )
    app.add_url_rule('/fuan-relatives', view_func=FuanRelativeListView.as_view('fuan_relative_list'))
    app.add_url_rule('/fuan-thp-results', view_func=FuanTHPResultListView.as_view('fuan_thp_result_list'))
