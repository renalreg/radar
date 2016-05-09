from radar.ukrdc_importer.app import RadarUKRDCImporter

app = RadarUKRDCImporter()
celery = app.celery
