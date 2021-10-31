import asyncio

from channels.db import database_sync_to_async

from students.models import Student
from students.utilities.starters import student_sync
from syncing.models import Signup
from syncing.utilities.status_codes import SignupStatusCodes


async def gather_with_concurrency(tasks, limit=32):
    semaphore = asyncio.Semaphore(limit)

    async def sem_task(task):
        async with semaphore:
            return await task

    return await asyncio.gather(*(sem_task(task) for task in tasks))


@database_sync_to_async
def get_all_students() -> list:
    return list(Student.objects.all().values("roll_number", "std_pass"))


@database_sync_to_async
def create_signup_for_student(roll_number, semester_list):
    user = Student.objects.get(roll_number=roll_number)

    signup_obj = Signup.objects.create(
        student=user,
        logs=SignupStatusCodes.NOT_YET_STARTED.value,
        attendance_pending=semester_list,
        result_pending=semester_list,
    )
    return signup_obj


async def sequence_starter(message):
    students = await get_all_students()

    tasks = []
    for student in students:
        tasks.append(
            asyncio.create_task(
                student_sync(
                    roll_number=student["roll_number"], password=student["std_pass"], isSyncing=True, message=message
                )
            )
        )
    res = await gather_with_concurrency(tasks)

    att_res_coroutines = [j for sub in res for j in sub]
    await gather_with_concurrency(att_res_coroutines, limit=24)
    message("Process Completed", "success")


async def admin_sync(roll_number, semester_list, message):
    signup = await create_signup_for_student(roll_number, semester_list)

    res = await student_sync(
        roll_number=signup.student.roll_number, password=signup.student.std_pass, isSyncing=False, message=message
    )
    await gather_with_concurrency(res)
    message("Process Completed", "success")
