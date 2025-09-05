#!/bin/bash
set -o errexit
pip install -r requirements.txt
cd $(dirname $(find . | grep manage.py$))
python manage.py migrate