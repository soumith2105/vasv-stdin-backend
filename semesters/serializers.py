from rest_framework import serializers

from .models import Semester


class SemesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semester
        fields = [
            "student",
            "semester",
            "internal1_max",
            "internal1",
            "internal1_per",
            "internal2_max",
            "internal2",
            "internal2_per",
            "assignment1_max",
            "assignment1",
            "assignment1_per",
            "assignment2_max",
            "assignment2",
            "assignment2_per",
            "assignment3_max",
            "assignment3",
            "assignment3_per",
            "quiz1_max",
            "quiz1",
            "quiz1_per",
            "quiz2_max",
            "quiz2",
            "quiz2_per",
            "quiz3_max",
            "quiz3",
            "quiz3_per",
            "session_max",
            "session",
            "session_per",
            "external_sub_credits",
            "external_grade_pts",
            "sgpa",
        ]
