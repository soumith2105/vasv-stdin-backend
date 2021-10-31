from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import Group

from students.models import Student

AdminSite.site_header = "DEETS 2.0 - Project02"
AdminSite.site_title = "Deets 2.0"
AdminSite.index_title = "Admin Portal"


class StudentAdmin(admin.ModelAdmin):
    exclude = ("std_pass",)
    readonly_fields = ("roll_number",)

    list_display = (
        "roll_number",
        "name",
        "branch",
        "current_year",
        "current_sem",
        "section",
        "current_status",
        "is_admin",
        "std_pass",
        "get_cgpa",
    )
    search_fields = (
        "roll_number",
        "name",
        "current_sem",
        "current_year",
        "branch",
    )
    list_filter = (
        "current_sem",
        "branch",
        "section",
        "current_status",
    )

    def get_cgpa(self, obj):
        if obj.cgpa == -1:
            return "Failed"
        return obj.cgpa

    get_cgpa.admin_order_field = "cgpa"
    get_cgpa.short_description = "CGPA"


admin.site.register(Student, StudentAdmin)
admin.site.unregister(Group)
