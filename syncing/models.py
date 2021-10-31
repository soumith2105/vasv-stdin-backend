from django.db import models

from semesters.models import Semester
from students.models import Student
from syncing.utilities.status_codes import FailedSyncStatusCodes, SignupStatusCodes, SyncStatusCodes


class Sync(models.Model):
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(auto_now_add=True)
    task_type = models.CharField(max_length=40, null=False, blank=False)
    persons_synced = models.IntegerField(default=0)
    persons_failed = models.IntegerField(default=0)
    status = models.CharField(default=SyncStatusCodes.IN_PROGRESS, max_length=40, blank=False)
    sync_per_cycle = models.IntegerField(default=16)


class Signup(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    synced_at = models.DateTimeField(null=True, blank=True)
    status = models.BooleanField(default=False)
    logs = models.CharField(max_length=40, default=SignupStatusCodes.NOT_YET_STARTED.value, blank=False)
    attendance_pending = models.CharField(max_length=15, blank=True, null=False, default="")
    result_pending = models.CharField(max_length=15, blank=True, null=False, default="")


class FailedSync(models.Model):
    status = models.CharField(max_length=40, default=FailedSyncStatusCodes.SYNC.value, blank=False)
    semester = models.OneToOneField(Semester, on_delete=models.CASCADE)
    logs = models.CharField(max_length=100)
