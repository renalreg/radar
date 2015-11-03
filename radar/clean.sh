#!/bin/bash

cd "$(dirname "$0")"

find . -name __pycache__ -delete
find . -name *.pyc -delete
