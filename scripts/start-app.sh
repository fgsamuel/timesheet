#!/bin/bash
set -e
python manage.py migrate
python manage.py collectstatic --no-input --clear
python manage.py seed
gunicorn timesheet.wsgi -b 0.0.0.0:8000
