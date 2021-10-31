from channels.db import database_sync_to_async

from semesters.models import Semester
from students.models import Student


@database_sync_to_async
def create_or_update_student(data):
    student = Student.objects.filter(roll_number=data["roll_number"])
    created = False
    if student.exists():
        student = student.first()
        student.roll_number = data["roll_number"]
        student.name = data["name"]
        student.current_year = data["current_year"]
        student.current_sem = data["current_sem"]
        student.branch = data["branch"]
        student.section = data["section"]
        student.current_status = data.get("current_status", "Studying")
        student.std_pass = data["password"]
        student.is_admin = data.get("admin", student.is_admin)
        student.save()

    else:
        student = Student(
            roll_number=data["roll_number"],
            name=data["name"],
            current_year=data["current_year"],
            current_sem=data["current_sem"],
            branch=data["branch"],
            section=data["section"],
            current_status=data.get("current_status", "Studying"),
            std_pass=data["password"],
        )
        student.is_admin = data.get("admin", student.is_admin)
        student.set_password(data["password"])
        student.save()
        created = True

    return student, created


@database_sync_to_async
def get_semesters_of_student(student):
    return list(
        Semester.objects.filter(student=student)
        .values("semester", "attendance_link", "result_link")
        .order_by("-semester")
    )
