#!/bin/bash

echo "Applying database migrations..."
python manage.py makemigrations --check
python manage.py migrate

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Django setup complete!"

python manage.py runserver 0.0.0.0:8000