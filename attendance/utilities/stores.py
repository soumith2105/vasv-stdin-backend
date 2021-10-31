from channels.db import database_sync_to_async

from attendance.models import Attendance, AttendanceBlock, Session
from semesters.models import Semester
from subjects.utilities.counter import count_subject_attendance
from subjects.models import Subject


@database_sync_to_async
def save_attendance_block(row):
    attendance_block = AttendanceBlock.objects.filter(
        semester=row["semester"],
        link=row["link"],
        total=row.get("total", 0),
        present=row.get("present", 0),
        absent=row.get("absent", 0),
        percent=row.get("percent", 0),
    )

    if not attendance_block.exists():

        attendance_block = AttendanceBlock.objects.filter(semester=row["semester"])
        if attendance_block.exists():

            attendance_block = attendance_block.first()

            attendance_block.link = row["link"]
            attendance_block.total = row.get("total", 0)
            attendance_block.present = row.get("present", 0)
            attendance_block.absent = row.get("absent", 0)
            attendance_block.percent = (row.get("percent", 0),)

            attendance_block.save()

            return attendance_block
        else:

            attendance_block = AttendanceBlock(
                semester=row["semester"],
                link=row["link"],
                total=row.get("total", 0),
                present=row.get("present", 0),
                absent=row.get("absent", 0),
                percent=row.get("percent", 0),
            )

            attendance_block.save()

            return attendance_block

    return attendance_block.first()


@database_sync_to_async
def get_attendance_block(row):
    attendance_block, _ = AttendanceBlock.objects.get_or_create(
        semester=row["semester"],
    )
    attendance_block.link = row["link"]
    attendance_block.save()
    return attendance_block


def convert_attendance_list_to_dict(attendance_list):
    attendance_dict = {}
    for obj in attendance_list:
        attendance_dict[obj.date] = obj

    return attendance_dict


@database_sync_to_async
def save_session(
    attendance_block: AttendanceBlock,
    semester: Semester,
    attendance_stats: dict,
    branch,
):
    # getting all attendance objects currently available in db -> converted to dict
    attendance_dates_dict = convert_attendance_list_to_dict(
        Attendance.objects.filter(attendance_block=attendance_block)
    )

    all_dates = set(attendance_stats["sessions"].keys())
    deletions = []
    changes = []
    sessions = attendance_stats["sessions"]
    for date_obj in attendance_dates_dict:
        if date_obj in all_dates:
            attendance_model = attendance_dates_dict[date_obj]
            if (
                attendance_model.present != sessions[date_obj]["present"]
                or attendance_model.absent != sessions[date_obj]["absent"]
                or attendance_model.total != sessions[date_obj]["total"]
            ):
                attendance_model.present = sessions[date_obj]["present"]
                attendance_model.absent = sessions[date_obj]["absent"]
                attendance_model.total = sessions[date_obj]["total"]
                changes.append(attendance_model)

            all_dates.remove(date_obj)
        else:
            deletions.append(date_obj)
            del attendance_dates_dict[date_obj]

    # deletions if any row got deleted in current attendance records
    if len(deletions):
        Attendance.objects.filter(attendance_block=attendance_block, date__in=deletions).delete()

    # changes if any row got deleted in current attendance records
    if len(changes) > 0:
        Attendance.objects.bulk_update(changes, fields=["present", "absent", "total"])

    # create attendance objects if not present and delete objects if not present in current attendance records
    if len(all_dates) > 0:
        creations = [
            Attendance(
                date=obj,
                attendance_block=attendance_block,
                present=sessions[obj]["present"],
                absent=sessions[obj]["absent"],
                total=sessions[obj]["total"],
            )
            for obj in all_dates
        ]

        Attendance.objects.bulk_create(creations)

        # get newly created attendance objects and merge both dicts to get all obj
        created_attendance_dates_dict = convert_attendance_list_to_dict(
            Attendance.objects.filter(attendance_block=attendance_block, date__in=all_dates)
        )
        attendance_dates_dict.update(created_attendance_dates_dict)

    # get all the subjects of entire semester
    subject_models = {}
    subject_objects = Subject.objects.filter(semester=semester.semester, branch=branch)
    subject_dict = attendance_stats["subjects"].copy()
    for subject_object in subject_objects:
        for subject in subject_dict:
            if subject == subject_object.name:
                subject_models[subject_object.name] = {
                    "model": subject_object,
                    "present": attendance_stats["subjects"][subject_object.name]["present"],
                    "absent": attendance_stats["subjects"][subject_object.name]["absent"],
                }
                del subject_dict[subject]
                break

    # create subjects if not present in db
    if len(subject_dict.keys()) > 0:
        creations = [
            Subject(
                name=subject,
                semester=semester.semester,
                branch=branch,
                section=semester.student.section,
                year=semester.year,
            )
            for subject in subject_dict
        ]

        Subject.objects.bulk_create(creations)
        new_subjects = Subject.objects.filter(name__in=subject_dict.keys())

        for new_subject in new_subjects:
            subject_models[new_subject.name] = {
                "model": new_subject,
                "present": attendance_stats["subjects"][new_subject.name]["present"],
                "absent": attendance_stats["subjects"][new_subject.name]["absent"],
            }

    # get all existing sessions of entire semester
    existing_attendance_rows = list(
        Session.objects.filter(attendance__attendance_block=attendance_block).order_by("attendance__date")
    )

    creations = []
    changes = []

    for day_sessions in sorted(sessions):
        for session in sessions[day_sessions]["classes"]:
            found = False
            for existing_row in existing_attendance_rows:

                if (
                    existing_row.attendance.date == day_sessions
                    and existing_row.start == session["start"]
                    and existing_row.end == session["end"]
                ):

                    found = True
                    if (
                        existing_row.subject != subject_models[session["subject"]]["model"]
                        or existing_row.did_attend != session["did_attend"]
                    ):
                        existing_row.subject = subject_models[session["subject"]]["model"]
                        existing_row.did_attend = session["did_attend"]
                        changes.append(existing_row)

                    existing_attendance_rows.remove(existing_row)
                    break

            if not found:
                creations.append(
                    Session(
                        attendance=attendance_dates_dict[day_sessions],
                        subject=subject_models[session["subject"]]["model"],
                        start=session["start"],
                        end=session["end"],
                        did_attend=session["did_attend"],
                    )
                )

    # if sessions are not in db then create
    if len(creations):
        Session.objects.bulk_create(creations)

    # if any changes in sessions
    if len(changes) > 0:
        Session.objects.bulk_update(changes, ["subject", "did_attend"])

    # if present in db and not present in current attendance sheet
    if len(existing_attendance_rows) > 0:
        delete_ele_ids = [att.id for att in existing_attendance_rows]
        Session.objects.filter(id__in=delete_ele_ids).delete()

    count_subject_attendance(semester=semester, subject_models=subject_models)
    attendance_block.total = attendance_stats["total"]
    attendance_block.present = attendance_stats["present"]
    attendance_block.absent = attendance_stats["absent"]
    attendance_block.percent = attendance_stats["percent"]
    attendance_block.save()


@database_sync_to_async
def get_attendance_links_of_semester(student):
    results = Semester.objects.filter(student=student)
    final = []
    for i in range(len(results)):
        obj = {
            "sem": results[i].semester,
            "link": AttendanceBlock.objects.get(semester=results[i]).link,
        }
        final.append(obj)

    return final
