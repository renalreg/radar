from radar_ukrdc_exporter.tasks import celery
from radar_ukrdc_exporter.app import setup_celery


setup_celery(celery)
