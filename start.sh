#!/bin/bash
set -e

echo "Running migrations..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting Gunicorn..."
exec gunicorn horilla.wsgi:application \
  --bind 0.0.0.0:$PORT \
  --workers 3 \
  --threads 2 \
  --timeout 120 \
  --preload
