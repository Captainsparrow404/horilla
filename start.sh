#!/bin/bash

set -e  # Exit on any error

echo "Making migrations for all apps..."
python manage.py makemigrations --noinput

echo "Applying database migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting Gunicorn with Scheduler..."

# Start Gunicorn in background
gunicorn horilla.wsgi:application --bind 0.0.0.0:$PORT &

# Delay to ensure Gunicorn is up
sleep 5

# Start Django scheduler
python manage.py shell -c "from leave.scheduler import start_scheduler; start_scheduler()"
