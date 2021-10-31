from django.contrib.auth import login, logout
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.status import HTTP_200_OK, HTTP_204_NO_CONTENT
from rest_framework.views import APIView, Response

from students.models import Student
from students.serializers import (
    StudentDetailsSerializer,
    StudentLoginSerializer,
    StudentSignupSerializer,
)


class StudentInfoAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = StudentDetailsSerializer

    def get_queryset(self):
        return self.request.user

    def get_object(self):
        return self.request.user

    class Meta:
        model = Student


class LoginUserAPIView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = (
        TokenAuthentication,
        SessionAuthentication,
    )
    serializer_class = StudentLoginSerializer

    def post(self, request):
        serializer = StudentLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key}, status=HTTP_200_OK)

    class Meta:
        model = Student


class LogoutUserAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = (
        TokenAuthentication,
        SessionAuthentication,
    )

    def post(self, request):
        token = Token.objects.get(user=request.user)
        token.delete()
        logout(request)
        return Response(status=HTTP_204_NO_CONTENT)

    class Meta:
        model = Student


class SignupUserAPIView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = StudentSignupSerializer
    queryset = Student.objects.all()

    class Meta:
        model = Student
