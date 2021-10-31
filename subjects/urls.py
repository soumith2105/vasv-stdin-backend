from django.urls import path

from subjects.views import SemesterMarks

urlpatterns = [
    path("marks/", SemesterMarks.as_view(), name="semester_marks"),
]

