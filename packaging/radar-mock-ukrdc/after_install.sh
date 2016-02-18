#!/bin/sh

set -e

systemctl daemon-reload
systemctl start radar-mock-ukrdc
