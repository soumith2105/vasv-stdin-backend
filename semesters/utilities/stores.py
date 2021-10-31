from channels.db import database_sync_to_async

from semesters.models import Semester, SemesterBlock


@database_sync_to_async
def get_semester(student, semester_number) -> Semester:
    semester = Semester.objects.filter(student=student, semester=semester_number)

    if not semester.exists():
        semester, _ = Semester.objects.get_or_create(student=student, semester=semester_number)
        return semester

    semester = semester.first()
    return semester


@database_sync_to_async
def update_semester(
    student,
    semester_number,
    result_link=None,
    year=None,
    attendance_link=None,
    start_date=None,
    end_date=None,
    current_status=None,
):

    semester = Semester.objects.get(student=student, semester=semester_number)
    if result_link:
        semester.result_link = result_link
    if attendance_link:
        semester.attendance_link = attendance_link
    if year:
        semester.year = year
    if start_date:
        semester.start_date = start_date
    if end_date:
        semester.end_date = end_date
    if current_status is not None and semester.current_status != current_status:
        semester.current_status = current_status

    semester.save()


@database_sync_to_async
def save_semester_marks(semester, data):
    semester_block = SemesterBlock.objects.filter(
        semester=semester,
        int1_max=data.get("int1_max", 0),
        int1=data.get("int1", 0),
        int2_max=data.get("int2_max", 0),
        int2=data.get("int2", 0),
        assn1_max=data.get("assn1_max", 0),
        assn1=data.get("assn1", 0),
        assn2_max=data.get("assn2_max", 0),
        assn2=data.get("assn2", 0),
        assn3_max=data.get("assn3_max", 0),
        assn3=data.get("assn3", 0),
        quiz1_max=data.get("quiz1_max", 0),
        quiz1=data.get("quiz1", 0),
        quiz2_max=data.get("quiz2_max", 0),
        quiz2=data.get("quiz2", 0),
        quiz3_max=data.get("quiz3_max", 0),
        quiz3=data.get("quiz3", 0),
        sess_max=data.get("sess_max", 0),
        sess=data.get("sess", 0),
        sess_per=data.get("sess_per", 0),
        ext_sub_credits=data.get("ext_sub_credits", 0),
        ext_grade_pts=data.get("ext_grade_pts", 0),
        sgpa=data.get("sgpa", 0),
    )
    if not semester_block.exists():
        semester_block, created = SemesterBlock.objects.get_or_create(semester=semester)
        semester_block.int1_max = data.get("int1_max", 0)
        semester_block.int1 = data.get("int1", 0)
        semester_block.int2_max = data.get("int2_max", 0)
        semester_block.int2 = data.get("int2", 0)
        semester_block.assn1_max = data.get("assn1_max", 0)
        semester_block.assn1 = data.get("assn1", 0)
        semester_block.assn2_max = data.get("assn2_max", 0)
        semester_block.assn2 = data.get("assn2", 0)
        semester_block.assn3_max = data.get("assn3_max", 0)
        semester_block.assn3 = data.get("assn3", 0)
        semester_block.quiz1_max = data.get("quiz1_max", 0)
        semester_block.quiz1 = data.get("quiz1", 0)
        semester_block.quiz2_max = data.get("quiz2_max", 0)
        semester_block.quiz2 = data.get("quiz2", 0)
        semester_block.quiz3_max = data.get("quiz3_max", 0)
        semester_block.quiz3 = data.get("quiz3", 0)
        semester_block.sess_max = data.get("sess_max", 0)
        semester_block.sess = data.get("sess", 0)
        semester_block.sess_per = data.get("sess_per", 0)
        semester_block.ext_sub_credits = data.get("ext_sub_credits", 0)
        semester_block.ext_grade_pts = data.get("ext_grade_pts", 0)
        semester_block.sgpa = data.get("sgpa", None)

        semester_block.save()


def calculate_cgpa(student):
    semesters = SemesterBlock.objects.filter(semester__student=student)
    aggregate_cgpa = 0
    sem_count = 0
    sem_nulls = 0
    for semester in semesters:
        if semester.sgpa == 0:
            student.cgpa = "NCLR"
            student.save()
            return
        elif semester.sgpa is None:
            sem_nulls += 1
        else:
            aggregate_cgpa += semester.sgpa
            sem_count += 1

    if sem_nulls == semesters.count():
        student.cgpa = None
    else:
        student.cgpa = round(aggregate_cgpa / sem_count, 3)
    student.save()
