#!/usr/bin/env bash
set -e
python /code/backend/manage.py migrate
python /code/backend/manage.py collectstatic --noinput
python /code/backend/manage.py runserver 0.0.0.0:8000