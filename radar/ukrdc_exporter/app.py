from radar.app import Radar
from radar.config import ConfigError


def check_config(config):
    if config.get('UKRDC_EXPORTER_URL') is None:
        raise ConfigError('Missing UKRDC_EXPORTER_URL')

    config.setdefault('UKRDC_EXPORTER_STATE', None)


class RadarUKRDCExporter(Radar):
    def check_config(self):
        super(RadarUKRDCExporter, self).check_config()
        check_config(self.config)
