from radar_api.serializers.consultants import ConsultantSerializer
from radar.views.core import ListModelView, RetrieveModelView
from radar.models import Consultant


class ConsultantListView(ListModelView):
    serializer_class = ConsultantSerializer
    model_class = Consultant


class ConsultantDetailView(RetrieveModelView):
    serializer_class = ConsultantSerializer
    model_class = Consultant
