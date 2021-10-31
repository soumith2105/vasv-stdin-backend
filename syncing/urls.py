from django.urls import path

from syncing.views import CheckSignup

urlpatterns = [
    path("status/", CheckSignup.as_view(), name="sync_check"),
]
