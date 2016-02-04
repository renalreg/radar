#!/bin/sh

set -e

systemctl daemon-reload
systemctl restart radar-api
