from subjects.models import SubjectBlock


def count_subject_attendance(semester, subject_models):
    subject_blocks = list(SubjectBlock.objects.filter(semester=semester))

    changes = []

    for subject_block in subject_blocks:
        subject = subject_models.get(subject_block.subject.name, None)
        if subject:
            subject_block.present = subject["present"]
            subject_block.absent = subject["absent"]
            subject_block.total = subject["present"] + subject["absent"]

            changes.append(subject_block)

            del subject_models[subject_block.subject.name]

    creations = []

    for subject_model in subject_models:
        subject = subject_models[subject_model]
        subject_block = SubjectBlock(
            semester=semester,
            subject=subject["model"],
            present=subject["present"],
            absent=subject["absent"],
            total=subject["present"] + subject["absent"],
        )
        creations.append(subject_block)

    SubjectBlock.objects.bulk_create(creations)
    SubjectBlock.objects.bulk_update(changes, fields=["present", "absent", "total"])
