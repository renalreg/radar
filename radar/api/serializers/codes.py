from cornflake.sqlalchemy_orm import ModelSerializer

from radar.models.codes import Code


class CodeSerializer(ModelSerializer):
    class Meta(object):
        model_class = Code
