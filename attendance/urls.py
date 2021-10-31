from django.urls import include, path

from attendance.views import AttendanceBlockAdminAPIView

admin_patterns = [
    path("sessions/", AttendanceBlockAdminAPIView.as_view(), name="sessions"),
]

urlpatterns = [
    path("admin/", include(admin_patterns)),
]
