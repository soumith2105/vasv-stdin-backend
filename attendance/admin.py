from django.contrib import admin
from django.utils.html import format_html

from .models import Attendance, AttendanceBlock, Session


class AttendanceBlockAdmin(admin.ModelAdmin):
    list_display = (
        "get_student",
        "get_semester",
        "total",
        "present",
        "absent",
        "percent",
        "show_attendance_url",
        "updated_at",
    )

    search_fields = ["semester__student__name", "semester__student__roll_number"]

    list_filter = [
        "semester__semester",
        "semester__student__branch",
        "semester__student__section",
    ]

    def show_attendance_url(self, obj):
        return format_html('<a href="%s" target="_blank">Open</a>' % obj.link)

    show_attendance_url.allow_tags = True
    show_attendance_url.short_description = "Link"

    def get_student(self, obj):
        return obj.semester.student.name

    get_student.admin_order_field = "semester__student__name"
    get_student.short_description = "Student Name"

    def get_semester(self, obj):
        return obj.semester.semester

    get_semester.admin_order_field = "semester__semester"
    get_semester.short_description = "Semester"


admin.site.register(AttendanceBlock, AttendanceBlockAdmin)


class SessionAdminInline(admin.TabularInline):
    model = Session
    extra = 0


class AttendanceAdmin(admin.ModelAdmin):

    inlines = (SessionAdminInline,)

    list_display = (
        "get_student",
        "get_semester",
        "date",
        "session_display",
        "present",
        "absent",
        "total",
    )

    search_fields = ["attendance_block__semester__student__name", "attendance_block__semester__student__roll_number"]

    list_filter = [
        "attendance_block__semester__semester",
        "attendance_block__semester__student__branch",
        "attendance_block__semester__student__section",
    ]

    def get_student(self, obj):
        return obj.attendance_block.semester.student.name

    get_student.admin_order_field = "attendance_block__semester__student__name"
    get_student.short_description = "Student Name"

    def get_semester(self, obj):
        return obj.attendance_block.semester.semester

    get_semester.admin_order_field = "attendance_block__semester__semester"
    get_semester.short_description = "Semester"

    def session_display(self, obj):
        sess = []
        for session in obj.sessions.all():
            icon = '<img src="/static/admin/img/icon-no.svg" alt="False">'
            if session.did_attend:
                icon = '<img src="/static/admin/img/icon-yes.svg" alt="True">'

            text = f"{icon} {session.subject.name} <br/> ({session.start} - {session.end})"
            string = f'<p style="margin:0; width: 100px;">{text}</p>'

            sess.append(string)

        return format_html(f'<div style="display: flex;">{"".join(sess)}</div>')

    session_display.short_description = "Sessions"


admin.site.register(Attendance, AttendanceAdmin)

#
# class SessionAdmin(admin.ModelAdmin):
#     list_display = (
#         "get_student",
#         "get_semester",
#         "get_date",
#         "subject",
#         "did_attend",
#         "start",
#         "end",
#     )
#
#     search_fields = [
#         "attendance__attendance_block__semester__student__name",
#         "attendance__attendance_block__semester__student__roll_number",
#     ]
#
#     list_filter = [
#         "attendance__attendance_block__semester__semester",
#         "attendance__attendance_block__semester__student__branch",
#         "attendance__attendance_block__semester__student__section",
#     ]
#
#     def get_student(self, obj):
#         return obj.attendance.attendance_block.semester.student.name
#
#     get_student.admin_order_field = "attendance__attendance_block__semester__student__name"
#     get_student.short_description = "Student Name"
#
#     def get_semester(self, obj):
#         return obj.attendance.attendance_block.semester.semester
#
#     get_semester.admin_order_field = "attendance__attendance_block__semester__semester"
#     get_semester.short_description = "Semester"
#
#     def get_date(self, obj):
#         return obj.attendance.date
#
#     get_date.admin_order_field = "attendance__date"
#     get_date.short_description = "Date"
#
#
# admin.site.register(Session, SessionAdmin)
