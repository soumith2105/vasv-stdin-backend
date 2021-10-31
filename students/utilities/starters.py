from channels.db import database_sync_to_async
from rest_framework.authtoken.models import Token
from vasvscrapper.status_codes.login import LOGIN_SUCCESS

from attendance.utilities.attendance_helper import attendance_function
from students.utilities.stores import create_or_update_student, get_semesters_of_student
from subjects.utilities.result_helper import result_function
from vasvscrapper.login import login_student


@database_sync_to_async
def get_token(student):
    token, created = Token.objects.get_or_create(user=student)
    return token, created


async def check_semesters_to_update(existing_data, current_data):
    attendance_sync_list = []
    result_sync_list = []

    for current in current_data:
        result_found = False
        attendance_found = False
        for existing in existing_data:
            if existing["semester"] == current["sem"]:
                if existing["attendance_link"] == current["attendance_link"]:
                    attendance_found = True

                if existing["result_link"] == current["result_link"]:
                    result_found = True

        if not attendance_found:
            attendance_sync_list.append(current)

        if not result_found:
            result_sync_list.append(current)

    return attendance_sync_list, result_sync_list


async def student_sync(roll_number, password, isSyncing, message):
    data = await login_student(roll_number=roll_number, password=password)
    if data["status"] == LOGIN_SUCCESS:
        data["password"] = password
        student, created = await create_or_update_student(data=data)

        if created:
            message("User Created Successfully", "success")

        attendance_sync_list = data["semesters"]
        result_sync_list = data["semesters"]

        if isSyncing:
            existing_data = await get_semesters_of_student(student)
            attendance_sync_list, result_sync_list = await check_semesters_to_update(existing_data, data["semesters"])

        result_sequences = await result_function(
            semesters=result_sync_list,
            student=student,
            branch=data["branch"],
            message=message,
        )
        attendance_sequences = await attendance_function(
            semesters=attendance_sync_list,
            student=student,
            branch=data["branch"],
            message=message,
        )

        return [*result_sequences, *attendance_sequences]
    else:
        message(data["status"], "error")
