#!/bin/sh

set -e

systemctl daemon-reload

# TODO check running
systemctl restart radar-mock-ukrdc
