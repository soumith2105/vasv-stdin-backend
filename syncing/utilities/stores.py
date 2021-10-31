from channels.db import database_sync_to_async
from django.utils import timezone

from semesters.models import Semester
from semesters.utilities.stores import calculate_cgpa
from students.models import Student
from syncing.models import Signup
from syncing.utilities.status_codes import SignupStatusCodes


@database_sync_to_async
def get_signup_for_attendance(student: Student, semester: Semester) -> None:
    signups = Signup.objects.filter(student=student, status=False)
    if signups.exists():
        signup = signups.first()

        attendance_semester_list = signup.attendance_pending.split(",")

        attendance_semester_list.remove(str(semester.semester))
        signup.attendance_pending = "" + ",".join(attendance_semester_list)

        signup.logs = SignupStatusCodes.IN_PROGRESS.value

        if signup.attendance_pending == signup.result_pending == "":
            signup.synced_at = timezone.now()
            signup.status = True
            signup.logs = SignupStatusCodes.SUCCESS.value

        signup.save()


@database_sync_to_async
def get_signup_for_result(student: Student, semester: Semester) -> None:
    signups = Signup.objects.filter(student=student, status=False)
    if signups.exists():
        signup = signups.first()
        result_semester_list = signup.result_pending.split(",")

        result_semester_list.remove(str(semester.semester))
        signup.result_pending = "" + ",".join(result_semester_list)

        signup.logs = SignupStatusCodes.IN_PROGRESS.value
        if signup.result_pending == "":
            calculate_cgpa(student=student)
            if signup.attendance_pending == "":
                signup.synced_at = timezone.now()
                signup.status = True
                signup.logs = SignupStatusCodes.SUCCESS.value

        signup.save()
