from radar_ukrdc_importer.tasks import celery
from radar_ukrdc_importer.app import setup_celery


setup_celery(celery)
