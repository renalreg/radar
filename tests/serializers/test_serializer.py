from radar.lib.serializers.core import Serializer, Empty
from radar.lib.serializers.fields import IntegerField


class FooModel(object):
    def __init__(self, foo=None, bar=None):
        if foo is not Empty:
            self.foo = foo

        if bar is not Empty:
            self.bar = bar


class FooSerializer(Serializer):
    foo = IntegerField()
    bar = IntegerField()
