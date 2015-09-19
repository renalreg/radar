from radar.api.serializers.results import ResultGroupSpecSerializer
from radar.lib.models import ResultGroupSpec
from radar.lib.views.core import ListModelView


class ResultGroupSpecListView(ListModelView):
    serializer_class = ResultGroupSpecSerializer
    model_class = ResultGroupSpec
