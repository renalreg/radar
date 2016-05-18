from radar.app import Radar
from radar.config import ConfigError


def check_config(config):
    if config.get('EXPORT_URL') is None:
        raise ConfigError('Missing EXPORT_URL')

    config.setdefault('EXPORT_STATE', None)


class RadarUKRDCExporter(Radar):
    def check_config(self):
        super(RadarUKRDCExporter, self).check_config()
        check_config(self.config)
