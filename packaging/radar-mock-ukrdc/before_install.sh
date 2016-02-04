#!/bin/sh

set -e

USER=radar
GROUP=radar

getent group $GROUP > /dev/null || groupadd -r $GROUP
getent passwd $USER > /dev/null || useradd -r -g $GROUP -d / -s /sbin/nologin $USER
