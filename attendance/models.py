from django.db import models

from semesters.models import Semester
from subjects.models import Subject


class AttendanceBlock(models.Model):
    semester = models.OneToOneField(Semester, on_delete=models.CASCADE)
    total = models.IntegerField(default=0)
    present = models.IntegerField(default=0)
    absent = models.IntegerField(default=0)
    percent = models.FloatField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["semester__student", "-semester__semester"]


class Attendance(models.Model):
    date = models.DateField()
    present = models.IntegerField(default=0)
    absent = models.IntegerField(default=0)
    total = models.IntegerField(default=0)
    attendance_block = models.ForeignKey(AttendanceBlock, on_delete=models.CASCADE, related_name="attendance")

    class Meta:
        ordering = ["attendance_block__semester__student", "-date"]
        verbose_name_plural = "Attendance"


class Session(models.Model):
    attendance = models.ForeignKey(Attendance, on_delete=models.CASCADE, related_name="sessions")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="subject")
    did_attend = models.BooleanField(null=True)
    start = models.CharField(max_length=20, blank=True, null=True)
    end = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        ordering = ["attendance__attendance_block__semester__student", "-attendance__date", "start"]
