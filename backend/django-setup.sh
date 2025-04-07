#!/bin/bash

echo "Applying database migrations..."
python manage.py migrate --noinput

if [ "$DJANGO_ENV" = "development" ]; then
    echo "Running makemigrations (only in development)..."
    python manage.py makemigrations
fi

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Django setup complete!"

if [ "$DJANGO_ENV" = "development" ]; then
    echo "Starting Django development server..."
    exec python manage.py runserver 0.0.0.0:8000
else
    echo "Starting Gunicorn server..."
    exec gunicorn backend.wsgi:application --bind 0.0.0.0:${PORT:-8080} --workers 4
fi
