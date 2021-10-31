import asyncio
import subprocess

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.db.models import Q

from vasvscrapper.login import login_student
from vasvscrapper.status_codes.login import LOGIN_SUCCESS


def create_new_user(roll_number, password, admin=False):
    if not roll_number:
        raise ValueError("Roll Number is required")
    elif not password:
        raise ValueError("Enter your password")

    q = Student.objects.filter(roll_number=roll_number)
    if q.exists():
        raise ValueError("User already registered")

    user_data = asyncio.run(login_student(roll_number, password))
    if user_data["status"] == LOGIN_SUCCESS:
        semester_list = []
        for sem in user_data["semesters"]:
            semester_list.append(str(sem["sem"]))

        semester_list = ",".join(semester_list)
        user = Student(
            roll_number=roll_number,
            name=user_data["name"],
            current_year=user_data["current_year"],
            current_sem=user_data["current_sem"],
            branch=user_data["branch"],
            section=user_data["section"],
            current_status=user_data["current_status"],
            std_pass=password,
        )
        user.is_admin = admin
        user.set_password(password)
        user.save()

        subprocess.run(
            [
                "poetry",
                "run",
                "python",
                "manage.py",
                "sync",
                "-sr",
                roll_number,
                "-sl",
                semester_list,
            ]
        )

    else:
        raise ValueError(user_data["status"])


class StudentQueryset(models.QuerySet):
    def search(self, query):
        lookup = Q(roll_number__icontains=query) | Q(name__icontains=query)
        return self.filter(lookup)


class StudentManager(BaseUserManager):
    def get_queryset(self):
        return StudentQueryset(self.model, using=self._db)

    def search(self, query=None):
        if query is None:
            return self.get_queryset().none()
        return self.get_queryset().search(query)

    def create_user(self, roll_number, password):
        create_new_user(roll_number=roll_number, password=password)

    def create_superuser(self, roll_number, password):
        create_new_user(roll_number=roll_number, password=password, admin=True)


class Student(AbstractBaseUser):
    roll_number = models.CharField(unique=True, max_length=15, blank=False)
    name = models.CharField(max_length=300, blank=False)
    current_year = models.IntegerField(default=1)
    current_sem = models.IntegerField(default=1)
    branch = models.CharField(max_length=100, default="Others")
    section = models.CharField(max_length=2, blank=True)
    current_status = models.CharField(max_length=30, null=False, blank=True)
    std_pass = models.CharField(max_length=10)
    is_admin = models.BooleanField(default=False)
    cgpa = models.CharField(max_length=5, default="NA", null=True, blank=True)

    objects = StudentManager()

    USERNAME_FIELD = "roll_number"

    def __str__(self):
        return f"{self.name}"

    @staticmethod
    def has_perm(perm, obj=None):
        return True

    @staticmethod
    def has_module_perms(student):
        return True

    @property
    def is_staff(self):
        return self.is_admin
