from django.contrib import admin
from django.utils.html import format_html

from .models import Semester, SemesterBlock


class SemesterAdmin(admin.ModelAdmin):
    list_display = (
        "get_student",
        "get_branch",
        "get_sem",
        "start_date",
        "end_date",
        "year",
        "current_status",
        "show_attendance_url",
        "show_marks_url",
    )
    search_fields = (
        "student__name",
        "student__roll_number",
        "semester",
        "student__branch",
    )

    list_filter = [
        "semester",
        "student__branch",
        "student__section",
    ]

    def show_marks_url(self, obj):
        return format_html('<a href="%s" target="_blank">Open</a>' % obj.result_link)

    show_marks_url.allow_tags = True
    show_marks_url.short_description = "Res"

    def show_attendance_url(self, obj):
        return format_html('<a href="%s" target="_blank">Open</a>' % obj.attendance_link)

    show_attendance_url.allow_tags = True
    show_attendance_url.short_description = "Att"

    def get_student(self, obj):
        return obj.student.name

    get_student.admin_order_field = "student__name"
    get_student.short_description = "Student Name"

    def get_sem(self, obj):
        return format_html(f'<p style="font-size:16px;margin: 0;"><b>Sem {obj.semester}</b>')

    get_sem.admin_order_field = "semester"
    get_sem.short_description = "Sem"

    def get_branch(self, obj):
        return obj.student.branch

    get_branch.admin_order_field = "student__branch"
    get_branch.short_description = "Branch"


admin.site.register(Semester, SemesterAdmin)


class SemesterBlockAdmin(admin.ModelAdmin):
    list_display = (
        "get_student",
        "get_branch",
        "get_sem",
        "get_int1",
        "get_int2",
        "get_asn1",
        "get_asn2",
        "get_asn3",
        "get_quiz1",
        "get_quiz2",
        "get_quiz3",
        "get_sess",
        "get_sess_per",
        "get_grades",
        "sgpa",
        "show_marks_url",
        "updated_at",
    )
    search_fields = (
        "semester__student__name",
        "semester__student__roll_number",
        "semester__semester",
        "semester__student__branch",
    )

    list_filter = [
        "semester__semester",
        "semester__student__branch",
        "semester__student__section",
    ]

    def show_marks_url(self, obj):
        return format_html('<a href="%s" target="_blank">Open</a>' % obj.semester.result_link)

    show_marks_url.allow_tags = True
    show_marks_url.short_description = "Res"

    def get_student(self, obj):
        return obj.semester.student.name

    get_student.admin_order_field = "semester__student__name"
    get_student.short_description = "Student Name"

    def get_sem(self, obj):
        return format_html(
            f'<p style="font-size:16px;margin: 0;text"><b>Sem {obj.semester.semester}</b>\
                </p><p style="text-align: center; margin: 0;">{obj.semester.year[0:4]}/{obj.semester.year[-2:]}</p>'
        )

    get_sem.admin_order_field = "semester__semester"
    get_sem.short_description = "Sem"

    def get_branch(self, obj):
        return obj.semester.student.branch

    get_branch.admin_order_field = "semester__student__branch"
    get_branch.short_description = "Branch"

    def get_int1(self, obj):
        return format_html(f"<b>{obj.int1}/{obj.int1_max}</b>")

    get_int1.admin_order_field = "int1"
    get_int1.short_description = "Int1"

    def get_int2(self, obj):
        return format_html(f"<b>{obj.int2}/{obj.int2_max}</b>")

    get_int2.admin_order_field = "int2"
    get_int2.short_description = "Int2"

    def get_asn1(self, obj):
        return format_html(f"<b>{obj.assn1}/{obj.assn1_max}</b>")

    get_asn1.admin_order_field = "assn1"
    get_asn1.short_description = "Asn1"

    def get_asn2(self, obj):
        return format_html(f"<b>{obj.assn2}/{obj.assn2_max}</b>")

    get_asn2.admin_order_field = "assn2"
    get_asn2.short_description = "Asn2"

    def get_asn3(self, obj):
        return format_html(f"<b>{obj.assn3}/{obj.assn3_max}</b>")

    get_asn3.admin_order_field = "assn3"
    get_asn3.short_description = "Asn3"

    def get_quiz1(self, obj):
        return format_html(f"<b>{obj.quiz1}/{obj.quiz1_max}</b>")

    get_quiz1.admin_order_field = "quiz1"
    get_quiz1.short_description = "Quiz1"

    def get_quiz2(self, obj):
        return format_html(f"<b>{obj.quiz2}/{obj.quiz2_max}</b>")

    get_quiz2.admin_order_field = "quiz2"
    get_quiz2.short_description = "Quiz2"

    def get_quiz3(self, obj):
        return format_html(f"<b>{obj.quiz3}/{obj.quiz3_max}</b>")

    get_quiz3.admin_order_field = "quiz3"
    get_quiz3.short_description = "Quiz3"

    def get_sess(self, obj):
        return format_html(f'<p style="text-align: center;">{obj.sess}/{obj.sess_max}</p>')

    get_sess.admin_order_field = "sess"
    get_sess.short_description = "Sessional"

    def get_sess_per(self, obj):
        return format_html(f'<p style="font-size:16px;margin: 0;"><b>{obj.sess_per}</b></p>')

    get_sess_per.admin_order_field = "sess_per"
    get_sess_per.short_description = "Sessional"

    def get_grades(self, obj):
        return f"{obj.ext_grade_pts}({obj.ext_sub_credits})"

    get_grades.admin_order_field = "ext_grade_pts"
    get_grades.short_description = "GP"


admin.site.register(SemesterBlock, SemesterBlockAdmin)
