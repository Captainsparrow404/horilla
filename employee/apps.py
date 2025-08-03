from django.apps import AppConfig
import sys

class EmployeeConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "employee"

    def ready(self):
        from django.db import connection
        from apscheduler.schedulers.background import BackgroundScheduler
        from employee.scheduler import update_experience, block_unblock_disciplinary

        # Avoid running during migrations/management commands
        if any(cmd in sys.argv for cmd in ['makemigrations', 'migrate', 'collectstatic', 'shell', 'createsuperuser']):
            return

        try:
            # Check if all required tables exist before running the scheduler
            with connection.cursor() as cursor:
                cursor.execute("SELECT to_regclass('employee_disciplinaryaction')")
                result = cursor.fetchone()
                if result and result[0] is not None:
                    scheduler = BackgroundScheduler()
                    scheduler.add_job(update_experience, 'interval', hours=4)
                    scheduler.add_job(block_unblock_disciplinary, 'interval', seconds=25)
                    scheduler.start()
                else:
                    print("[Scheduler] Skipped: DisciplinaryAction table not found")
        except Exception as e:
            print(f"[Scheduler Init Error] {e}")
