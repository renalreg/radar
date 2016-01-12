from radar.serializers.fields import LabelledStringField, LabelledIntegerField
from radar.views.core import ListView


class CodedStringListView(ListView):
    items = {}

    def get_items(self):
        return self.items

    def get_serializer(self):
        return LabelledStringField(self.get_items())

    def get_object_list(self):
        return self.get_items().keys()


class CodedIntegerListView(ListView):
    items = {}

    def get_items(self):
        return self.items

    def get_serializer(self):
        return LabelledIntegerField(self.get_items())

    def get_object_list(self):
        return self.get_items().keys()
