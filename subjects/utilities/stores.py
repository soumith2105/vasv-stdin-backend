from channels.db import database_sync_to_async

from subjects.models import Subject, SubjectBlock


@database_sync_to_async
def save_subject_marks(semester, branch, subjects):
    subject_models = list(
        Subject.objects.filter(
            semester=semester.semester,
            branch=branch,
            section=semester.student.section,
            year=semester.year,
        )
    )

    creations = []
    new_subjects = []

    for subject in subject_models:
        if subject.name in subjects:
            subjects[subject.name]["subject_model"] = subject

    for subject, value in subjects.items():
        if "subject_model" not in value:
            new_subject = Subject(
                name=subject,
                semester=semester.semester,
                branch=branch,
                section=semester.student.section,
                year=semester.year,
            )
            creations.append(new_subject)
            new_subjects.append(subject)

    Subject.objects.bulk_create(creations)
    new_subject_models = list(Subject.objects.filter(name__in=new_subjects))

    for subject in new_subject_models:
        if subject.name in subjects:
            subjects[subject.name]["subject_model"] = subject

    subject_blocks_models = list(SubjectBlock.objects.filter(semester=semester))

    changes = []

    for subject_block in subject_blocks_models:
        subject = subjects.get(subject_block.subject.name, None)
        if subject:
            subject_block.int1_max = subject.get("int1_max", 0)
            subject_block.int1 = subject.get("int1", 0)
            subject_block.int2_max = subject.get("int2_max", 0)
            subject_block.int2 = subject.get("int2", 0)
            subject_block.assn1_max = subject.get("assn1_max", 0)
            subject_block.assn1 = subject.get("assn1", 0)
            subject_block.assn2_max = subject.get("assn2_max", 0)
            subject_block.assn2 = subject.get("assn2", 0)
            subject_block.assn3_max = subject.get("assn3_max", 0)
            subject_block.assn3 = subject.get("assn3", 0)
            subject_block.quiz1_max = subject.get("quiz1_max", 0)
            subject_block.quiz1 = subject.get("quiz1", 0)
            subject_block.quiz2_max = subject.get("quiz2_max", 0)
            subject_block.quiz2 = subject.get("quiz2", 0)
            subject_block.quiz3_max = subject.get("quiz3_max", 0)
            subject_block.quiz3 = subject.get("quiz3", 0)
            subject_block.sess_max = subject.get("sess_max", 0)
            subject_block.sess = subject.get("sess", 0)
            subject_block.ext_grade = subject.get("ext_grade", 0)
            subject_block.ext_sub_credits = subject.get("ext_sub_credits", 0)
            subject_block.ext_grade_pts = subject.get("ext_grade_pts", 0)

            changes.append(subject_block)

            del subjects[subject_block.subject.name]

    creations = []

    for subject, value in subjects.items():
        subject_block = SubjectBlock(
            semester=semester,
            subject=value["subject_model"],
            int1_max=value.get("int1_max", 0),
            int1=value.get("int1", 0),
            int2_max=value.get("int2_max", 0),
            int2=value.get("int2", 0),
            assn1_max=value.get("assn1_max", 0),
            assn1=value.get("assn1", 0),
            assn2_max=value.get("assn2_max", 0),
            assn2=value.get("assn2", 0),
            assn3_max=value.get("assn3_max", 0),
            assn3=value.get("assn3", 0),
            quiz1_max=value.get("quiz1_max", 0),
            quiz1=value.get("quiz1", 0),
            quiz2_max=value.get("quiz2_max", 0),
            quiz2=value.get("quiz2", 0),
            quiz3_max=value.get("quiz3_max", 0),
            quiz3=value.get("quiz3", 0),
            sess_max=value.get("sess_max", 0),
            sess=value.get("sess", 0),
            ext_grade=value.get("ext_grade", 0),
            ext_sub_credits=value.get("ext_sub_credits", 0),
            ext_grade_pts=value.get("ext_grade_pts", 0),
        )
        creations.append(subject_block)

    SubjectBlock.objects.bulk_create(creations)
    SubjectBlock.objects.bulk_update(
        changes,
        fields=[
            "int1_max",
            "int1",
            "int2_max",
            "int2",
            "assn1_max",
            "assn1",
            "assn2_max",
            "assn2",
            "assn3_max",
            "assn3",
            "quiz1_max",
            "quiz1",
            "quiz2_max",
            "quiz2",
            "quiz3_max",
            "quiz3",
            "sess_max",
            "sess",
            "ext_grade",
            "ext_sub_credits",
            "ext_grade_pts",
        ],
    )
