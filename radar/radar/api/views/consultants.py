from radar.api.serializers.consultants import ConsultantSerializer
from radar.lib.views.core import ListModelView, RetrieveModelView
from radar.lib.models import Consultant


class ConsultantListView(ListModelView):
    serializer_class = ConsultantSerializer
    model_class = Consultant


class ConsultantDetailView(RetrieveModelView):
    serializer_class = ConsultantSerializer
    model_class = Consultant
