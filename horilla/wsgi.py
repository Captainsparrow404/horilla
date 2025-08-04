import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'horilla.settings')
application = get_wsgi_application()

# Start the scheduler
try:
    from leave.scheduler import start_scheduler
    start_scheduler()
except Exception as e:
    print(f"Scheduler failed to start: {e}")
