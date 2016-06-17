#!/bin/bash

set -e

cd "$(dirname "$0")"
platter build -r requirements.txt .
