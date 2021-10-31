from rest_framework import serializers

from subjects.models import SubjectBlock


class SemesterSubjectMarksSerializer(serializers.ModelSerializer):
    subject = serializers.SerializerMethodField()

    class Meta:
        model = SubjectBlock
        fields = [
            "subject",
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
        ]

    def get_subject(self, obj):
        return obj.subject.name
