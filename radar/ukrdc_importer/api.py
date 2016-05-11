from flask import request, abort, Blueprint

from radar.app import Radar
from radar.ukrdc_importer.serializers import ContainerSerializer
from radar.ukrdc_importer.utils import utc
from radar.ukrdc_importer.tasks import import_sda


api = Blueprint('ukrdc_importer', __name__)


@api.route('/import', methods=['POST'])
def import_():
    sda_container = request.get_json()

    if sda_container is None:
        abort(400)

    serializer = ContainerSerializer(data=sda_container)

    if not serializer.is_valid():
        abort(400)

    sequence_number = utc()
    task = import_sda.delay(sda_container, sequence_number)
    task_id = task.id

    return str(task_id)


@api.route('/status/<task_id>')
def status(task_id):
    result = import_sda.AsyncResult(task_id)
    done = int(result.ready())
    return str(done)


def create_app():
    app = Radar()
    app.register_blueprint(api)
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', debug=True)