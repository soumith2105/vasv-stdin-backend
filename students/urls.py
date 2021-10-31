from django.urls import path

from students.views import (
    LoginUserAPIView,
    LogoutUserAPIView,
    StudentInfoAPIView,
    SignupUserAPIView,
)

urlpatterns = [
    path("login/", LoginUserAPIView.as_view(), name="login"),
    path("logout/", LogoutUserAPIView.as_view(), name="logout"),
    path("signup/", SignupUserAPIView.as_view(), name="create"),
    path("", StudentInfoAPIView.as_view(), name="details"),
]

# websockets_urlpatterns = [
#     # path("ws/student/create/", StudentCreateWebSocket.as_asgi()),
#     path("ws/student/syncing/", StudentSyncNecessaryWebSocket.as_asgi()),
# ]
