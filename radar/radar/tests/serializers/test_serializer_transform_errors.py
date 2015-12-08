from radar.serializers.core import Serializer
from radar.serializers.fields import StringField, ListField


class BarSerializer(Serializer):
    x = StringField()


class BazSerializer(Serializer):
    x = StringField()


class FooSerializer(Serializer):
    x = BarSerializer()
    y = ListField(BazSerializer())


def test_transform_errors():
    serializer = FooSerializer()

    assert serializer.transform_errors({
        'aaa': ['I am ignored!'],
        'x': {
            '_': ['An error!'],
            'x': ['Another error!'],
            'bbb': ['I am also ignored!'],
        },
        'y': {
            '_': ['An error!'],
            1: {
                'x': ['Another error!'],
                'aaa': ['I am ignored!'],
            },
            'aaa': ['I am also ignored!'],
        }
    }) == {
        'x': {
            '_': ['An error!'],
            'x': ['Another error!'],
        },
        'y': {
            '_': ['An error!'],
            1: {
                'x': ['Another error!']
            }
        }
    }
