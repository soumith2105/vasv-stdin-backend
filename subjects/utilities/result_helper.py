import asyncio

from vasvscrapper.status_codes.results import RESULT_SUCCESS

from semesters.utilities.stores import save_semester_marks, update_semester
from subjects.utilities.stores import save_subject_marks

from vasvscrapper.results import get_result
from semesters.utilities.stores import get_semester
from syncing.utilities.stores import get_signup_for_result


async def get_results(semester, student, branch, message):
    try:
        results = await get_result(semester["result_link"])
        if results["status"] == RESULT_SUCCESS:
            current_status = "Studying"
            if results["total"].get("sgpa", None) is not None:
                if results["total"]["sgpa"] == 0:
                    current_status = "Failed"
                else:
                    current_status = "Completed"

            semester_model = await get_semester(student=student, semester_number=semester["sem"])

            await asyncio.gather(
                save_subject_marks(branch=branch, semester=semester_model, subjects=results["subjects"]),
                save_semester_marks(semester=semester_model, data=results["total"]),
            )
            await update_semester(
                student=student,
                semester_number=semester["sem"],
                result_link=semester["result_link"],
                current_status=current_status,
            )
            await get_signup_for_result(student=student, semester=semester_model)
            message(f'✓ Results [{student.roll_number} {student.name} - Sem {semester["sem"]}]', "success")
        else:
            message(
                f'✕ Results [{student.roll_number} {student.name} - Sem {semester["sem"]}({results["status"]})]',
                "error",
            )

    except asyncio.exceptions.CancelledError:
        message(f'✕ Results [{student.roll_number} {student.name} - Sem {semester["sem"]}]', "error")


async def result_function(semesters, student, branch, message):
    tasks = []
    for semester in semesters:
        tasks.append(get_results(semester=semester, student=student, branch=branch, message=message))

    return tasks
