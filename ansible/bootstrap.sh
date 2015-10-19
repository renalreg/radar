#!/bin/bash

sudo yum install -y -q epel-release
sudo yum install -y -q ansible

cd /home/vagrant/src/ansible
sudo PYTHONUNBUFFERED=1 ansible-playbook site.yml -i vagrant-hosts
