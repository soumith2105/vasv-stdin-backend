from vasvscrapper.attendance import get_attendance
from vasvscrapper.status_codes.attendance import ATTENDANCE_SUCCESS

from attendance.utilities.stores import get_attendance_block, save_session
from semesters.utilities.stores import get_semester, update_semester
from syncing.utilities.stores import get_signup_for_attendance


async def fetch_attendance(semester, student, branch, message):
    try:
        # Getting Semester model
        semester_model = await get_semester(student=student, semester_number=semester["sem"])

        total_attendance = {
            "semester": semester_model,
            "link": semester["attendance_link"],
        }

        # Saving AttendanceBlock
        attendance_block = await get_attendance_block(total_attendance)

        # Attendance Setup
        attendance_stats = await get_attendance(link=semester["attendance_link"])

        if attendance_stats["status"] == ATTENDANCE_SUCCESS:
            await save_session(attendance_block, semester_model, attendance_stats, branch)
            await get_signup_for_attendance(student=student, semester=semester_model)
            await update_semester(
                student=student,
                semester_number=semester["sem"],
                year=semester["year"],
                attendance_link=semester["attendance_link"],
                start_date=semester["start_date"],
                end_date=semester["end_date"],
            )
            message(f'✓ Attendance [{student.roll_number} {student.name} - Sem {semester["sem"]}]', "success")

        else:
            message(
                f'✕ Attendance [{student.roll_number} {student.name} - Sem {semester["sem"]}({attendance_stats["status"]})]',
                "error",
            )
    except Exception:
        message(f'✕ Attendance [{student.roll_number} {student.name} - Sem {semester["sem"]}]', "error")


async def attendance_function(semesters, student, branch, message):
    tasks = []
    for semester in semesters:
        tasks.append(fetch_attendance(semester=semester, student=student, branch=branch, message=message))

    return tasks
