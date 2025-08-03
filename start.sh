#!/bin/bash

echo "Applying database migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting Gunicorn with Scheduler..."

# Run Gunicorn and start the scheduler from Django shell
exec gunicorn horilla.wsgi:application --bind 0.0.0.0:$PORT &

# Delay to ensure server boots
sleep 5

# 🟢 Start scheduler via Django shell
python manage.py shell -c "from leave.scheduler import start_scheduler; start_scheduler()"
