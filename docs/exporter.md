# Exporter

Data can be exported from RADAR as CSV using the `radar-exporter` script.

Config files are kept in the [radar-exports](https://github.com/renalreg/radar-exports) (Private) repo.

```sh
mkdir RDR-374
RADAR_SETTINGS=/etc/radar-api/settings.py /srv/radar/current/bin/radar-exporter RDR-374.ini RDR-374
zip -r RDR-374.zip RDR-374
```
