import sys
from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from dateutil.relativedelta import relativedelta

def leave_reset():
    from leave.models import LeaveType

    today = datetime.now().date()
    leave_types = LeaveType.objects.filter(reset=True)

    for leave_type in leave_types:
        available_leaves = leave_type.employee_available_leave.all()
        for available_leave in available_leaves:
            if available_leave.reset_date == today:
                new_reset = available_leave.set_reset_date(today, available_leave)
                available_leave.reset_date = new_reset
                available_leave.update_carryforward()
                available_leave.save()

            if available_leave.expired_date and available_leave.expired_date <= today:
                new_expired = available_leave.set_expired_date(available_leave, today)
                available_leave.expired_date = new_expired
                available_leave.save()

        if leave_type.carryforward_expire_date and leave_type.carryforward_expire_date <= today:
            leave_type.carryforward_expire_date = leave_type.set_expired_date(today)
            leave_type.save()

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(leave_reset, "interval", seconds=20)
    scheduler.start()
