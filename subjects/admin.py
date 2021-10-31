from django.contrib import admin

from .models import Subject, SubjectBlock


class SubjectAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "full_name",
        "lecturer",
        "year",
        "semester",
        "branch",
        "section",
    )

    search_fields = (
        "name",
        "lecturer",
        "full_name",
    )

    list_filter = [
        "year",
        "semester",
        "branch",
        "section",
    ]


admin.site.register(Subject, SubjectAdmin)


class SubjectBlockAdmin(admin.ModelAdmin):
    list_display = (
        "get_student",
        "subject",
        "semester",
        "get_attendance",
        "get_int1",
        "get_int2",
        "get_asn1",
        "get_asn2",
        "get_asn3",
        "get_quiz1",
        "get_quiz2",
        "get_quiz3",
        "sess",
        "get_grades",
    )

    search_fields = (
        "subject__name",
        "semester__student__name",
        "semester__student__roll_number",
    )

    list_filter = [
        "semester__semester",
        "subject__branch",
        "semester__student__section",
    ]

    def get_student(self, obj):
        return obj.semester.student.name

    # get_student.admin_order_field = 'students'
    get_student.short_description = "Student Name"

    def get_attendance(self, obj):
        return f"{obj.total}(P:{obj.present}_A:{obj.absent})"

    get_attendance.admin_order_field = "total"
    get_attendance.short_description = "Attendance"

    def get_int1(self, obj):
        return f"{obj.int1}/{obj.int1_max}"

    get_int1.admin_order_field = "int1"
    get_int1.short_description = "Int1"

    def get_int2(self, obj):
        return f"{obj.int2}/{obj.int2_max}"

    get_int2.admin_order_field = "int2"
    get_int2.short_description = "Int2"

    def get_asn1(self, obj):
        return f"{obj.assn1}/{obj.assn1_max}"

    get_asn1.admin_order_field = "assn1"
    get_asn1.short_description = "Asn1"

    def get_asn2(self, obj):
        return f"{obj.assn2}/{obj.assn2_max}"

    get_asn2.admin_order_field = "assn2"
    get_asn2.short_description = "Asn2"

    def get_asn3(self, obj):
        return f"{obj.assn3}/{obj.assn3_max}"

    get_asn3.admin_order_field = "assn3"
    get_asn3.short_description = "Asn3"

    def get_quiz1(self, obj):
        return f"{obj.quiz1}/{obj.quiz1_max}"

    get_quiz1.admin_order_field = "quiz1"
    get_quiz1.short_description = "Quiz1"

    def get_quiz2(self, obj):
        return f"{obj.quiz2}/{obj.quiz2_max}"

    get_quiz2.admin_order_field = "quiz2"
    get_quiz2.short_description = "Quiz2"

    def get_quiz3(self, obj):
        return f"{obj.quiz3}/{obj.quiz3_max}"

    get_quiz3.admin_order_field = "quiz3"
    get_quiz3.short_description = "Quiz3"

    def get_grades(self, obj):
        return f"{obj.ext_grade}({obj.ext_grade_pts}*{obj.ext_sub_credits})"

    get_grades.admin_order_field = "ext_grade_pts"
    get_grades.short_description = "GP"


admin.site.register(SubjectBlock, SubjectBlockAdmin)
