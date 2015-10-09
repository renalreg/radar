#!/bin/sh

user='radar'
group='radar'

getent group $group > /dev/null || groupadd -r $group
getent passwd $user > /dev/null || useradd -r -g $group -d / -s /sbin/nologin $user
