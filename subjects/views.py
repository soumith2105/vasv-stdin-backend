from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from semesters.models import Semester
from subjects.models import SubjectBlock
from subjects.permissions import IsOwnerOnly
from subjects.serializers import SemesterSubjectMarksSerializer


class SemesterMarks(ListAPIView):
    permission_classes = [IsAuthenticated, IsOwnerOnly]
    serializer_class = SemesterSubjectMarksSerializer

    def get_queryset(self):
        semester = self.request.GET.get("semester")
        student = self.request.user
        semester = Semester.objects.filter(student=student, semester=semester)
        if semester.exists():
            semester = semester.first()
            return SubjectBlock.objects.filter(semester=semester)
        else:
            return []

    class Meta:
        model = SubjectBlock
