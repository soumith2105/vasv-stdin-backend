from django.contrib import admin

from syncing.models import Signup


class SignupAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "created_at",
        "synced_at",
        "status",
    )

    search_fields = ("student__name", "student__roll_number")

    list_filter = [
        "status",
    ]


admin.site.register(Signup, SignupAdmin)
