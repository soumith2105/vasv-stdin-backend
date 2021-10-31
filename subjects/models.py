from django.db import models

from semesters.models import Semester


class Subject(models.Model):
    name = models.CharField(max_length=20)
    full_name = models.CharField(max_length=100, null=True, blank=True)
    lecturer = models.CharField(max_length=150, null=True, blank=True)
    year = models.CharField(max_length=15, default="NA")
    semester = models.IntegerField()
    branch = models.CharField(max_length=5, default="IT")
    section = models.CharField(max_length=2, blank=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ["year", "semester", "branch", "section", "name"]


class SubjectBlock(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    total = models.IntegerField(default=0)
    present = models.IntegerField(default=0)
    absent = models.IntegerField(default=0)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)

    int1_max = models.FloatField(default=0)
    int1 = models.FloatField(default=0)

    int2_max = models.FloatField(default=0)
    int2 = models.FloatField(default=0)

    assn1_max = models.FloatField(default=0)
    assn1 = models.FloatField(default=0)

    assn2_max = models.FloatField(default=0)
    assn2 = models.FloatField(default=0)

    assn3_max = models.FloatField(default=0)
    assn3 = models.FloatField(default=0)

    quiz1_max = models.FloatField(default=0)
    quiz1 = models.FloatField(default=0)

    quiz2_max = models.FloatField(default=0)
    quiz2 = models.FloatField(default=0)

    quiz3_max = models.FloatField(default=0)
    quiz3 = models.FloatField(default=0)

    sess_max = models.FloatField(default=0)
    sess = models.FloatField(default=0)

    ext_grade = models.CharField(max_length=3, default="NA", blank=False, null=False)
    ext_sub_credits = models.IntegerField(default=0)
    ext_grade_pts = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.subject}"

    class Meta:
        ordering = ["-semester__semester", "-semester__student__name", "subject__name"]
