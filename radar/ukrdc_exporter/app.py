from radar.app import Radar
from radar.config import ConfigError


def check_config(config):
    if config.get('UKRDC_IMPORT_URL') is None:
        raise ConfigError('Missing UKRDC_IMPORT_URL')


class RadarUKRDCExporter(Radar):
    def check_config(self):
        super(RadarUKRDCExporter, self).check_config()
        check_config(self.config)
