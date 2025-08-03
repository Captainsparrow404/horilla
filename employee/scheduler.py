import datetime
from datetime import timedelta

def update_experience():
    from employee.models import EmployeeWorkInformation

    queryset = EmployeeWorkInformation.objects.filter(employee_id__is_active=True)
    for instance in queryset:
        instance.experience_calculator()

def block_unblock_disciplinary():
    try:
        from base.models import EmployeeShiftSchedule
        from employee.models import DisciplinaryAction
        from employee.policies import employee_account_block_unblock

        dis_action = DisciplinaryAction.objects.all()
        for dis in dis_action:
            if dis.action.block_option:
                if dis.action.action_type == "suspension":
                    if dis.days:
                        end_date = dis.start_date + timedelta(days=dis.days)
                        if datetime.date.today() >= dis.start_date:
                            r = False
                        if datetime.date.today() >= end_date:
                            r = True
                        for emp in dis.employee_id.all():
                            employee_account_block_unblock(emp_id=emp.id, result=r)

                    if dis.hours:
                        hour_str = dis.hours + ":00"
                        if hour_str > "00:00:00" and datetime.date.today() >= dis.start_date:
                            for emp in dis.employee_id.all():
                                shift = emp.employee_work_info.shift_id
                                shift_detail = EmployeeShiftSchedule.objects.filter(shift_id=shift)
                                for shi in shift_detail:
                                    weekday_names = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
                                    if weekday_names[datetime.datetime.today().weekday()] == shi.day.day:
                                        st_time = shi.start_time
                                        hour_time = datetime.datetime.strptime(hour_str, "%H:%M:%S").time()

                                        datetime1 = datetime.datetime.combine(datetime.date.today(), st_time)
                                        datetime2 = datetime.datetime.combine(datetime.date.today(), hour_time)

                                        result_datetime = datetime1 + datetime.timedelta(
                                            hours=datetime2.hour,
                                            minutes=datetime2.minute,
                                            seconds=datetime2.second,
                                        )

                                        current_time = datetime.datetime.now().time()
                                        r = current_time >= result_datetime
                                        employee_account_block_unblock(emp_id=emp.id, result=r)

                elif dis.action.action_type == "dismissal" and datetime.date.today() >= dis.start_date:
                    for emp in dis.employee_id.all():
                        employee_account_block_unblock(emp_id=emp.id, result=False)

    except Exception as e:
        # Log this exception instead of crashing
        print(f"[Scheduler Error] block_unblock_disciplinary failed: {e}")
