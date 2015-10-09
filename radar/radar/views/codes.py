from radar.serializers.codes import CodedStringSerializer, CodedIntegerSerializer
from radar.views.core import ListView


class CodedStringListView(ListView):
    items = {}

    def get_items(self):
        return self.items

    def get_serializer(self):
        return CodedStringSerializer(self.get_items())

    def get_object_list(self):
        return self.get_items().keys()


class CodedIntegerListView(ListView):
    items = {}

    def get_items(self):
        return self.items

    def get_serializer(self):
        return CodedIntegerSerializer(self.get_items())

    def get_object_list(self):
        return self.get_items().keys()
