#!/bin/bash

# Apply migrations to the database
echo "Applying database migrations..."
python manage.py makemigrations --check
python manage.py migrate

# Collect static files into the static directory
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Create a superuser if needed (optional)
# python manage.py createsuperuser --noinput

echo "Django setup complete!"
