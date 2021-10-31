from rest_framework import serializers

from attendance.models import Attendance, AttendanceBlock, Session


class SessionSerializer(serializers.ModelSerializer):
    subject = serializers.SerializerMethodField()

    class Meta:
        model = Session
        fields = [
            "subject",
            "start",
            "end",
            "did_attend",
        ]

    def get_subject(self, obj):
        return obj.subject.name


class AttendanceSerializer(serializers.ModelSerializer):
    sessions = SessionSerializer(many=True)

    class Meta:
        model = Attendance
        fields = [
            "date",
            "present",
            "absent",
            "total",
            "sessions",
        ]

    def get_subject(self, obj):
        return obj.subject.name


class AttendanceBlockSerializer(serializers.ModelSerializer):
    attendance = AttendanceSerializer(many=True)
    semester = serializers.SerializerMethodField()

    class Meta:
        model = AttendanceBlock
        fields = [
            "semester",
            "link",
            "total",
            "present",
            "absent",
            "percent",
            "updated_at",
            "attendance",
        ]

    def get_semester(self, obj):
        return obj.semester.semester
