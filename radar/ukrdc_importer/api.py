import logging

from flask import abort, Blueprint, request, Response

from radar.app import Radar
from radar.ukrdc_importer.serializers import ContainerSerializer
from radar.ukrdc_importer.tasks import import_sda
from radar.ukrdc_importer.utils import utc


api = Blueprint("ukrdc_importer", __name__)


@api.route("/import", methods=["POST"])
def import_():
    sda_container = request.get_json()

    if sda_container is None:
        abort(400)

    serializer = ContainerSerializer(data=sda_container)

    if not serializer.is_valid():
        print(serializer.errors)
        abort(400)

    sequence_number = utc()
    import_sda.delay(sda_container, sequence_number)

    return Response(status=200)


def create_app():
    app = Radar()

    app.register_blueprint(api)

    if not app.debug:
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        app.logger.addHandler(stream_handler)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5001)
