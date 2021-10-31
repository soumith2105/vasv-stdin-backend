from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView

from syncing.models import Signup


class CheckSignup(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        signup_object = Signup.objects.filter(student=request.user)
        if signup_object.exists():
            return Response({"status": signup_object.first().status}, status=HTTP_200_OK)

        return ValueError("Student not signed up")

    class Meta:
        model = Signup
