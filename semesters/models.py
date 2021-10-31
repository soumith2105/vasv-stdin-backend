from django.db import models

from students.models import Student


class Semester(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    semester = models.IntegerField()
    year = models.CharField(max_length=15, default="NA")
    current_status = models.CharField(max_length=100, default="Studying")
    result_link = models.URLField(max_length=300, null=False, blank=False, default="http://vce.ac.in/")
    attendance_link = models.URLField(max_length=300, null=False, blank=False, default="http://vce.ac.in/")
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.semester}"

    class Meta:
        ordering = ["student__roll_number", "-semester"]


class SemesterBlock(models.Model):
    semester = models.OneToOneField(Semester, on_delete=models.CASCADE)
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
    sess_per = models.FloatField(default=0)
    ext_sub_credits = models.IntegerField(default=0)
    ext_grade_pts = models.IntegerField(default=0)
    sgpa = models.FloatField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.semester.student.roll_number} - {self.sgpa}"

    class Meta:
        ordering = ["semester__student__roll_number", "-semester__semester"]
