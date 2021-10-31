import asyncio

from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import NotAcceptable, ValidationError
from vasvscrapper.login import login_student
from vasvscrapper.status_codes.login import LOGIN_SUCCESS

from students.models import Student
from students.utilities.status_codes import (
    PASSWORD_REQUIRED,
    ROLL_NUMBER_REQUIRED,
    USER_ALREADY_EXISTS,
    USER_SIGNUP_SUCCESSFUL,
)
from syncing.models import Signup
from syncing.utilities.status_codes import SignupStatusCodes


class StudentDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = [
            "roll_number",
            "name",
            "current_year",
            "current_sem",
            "branch",
            "section",
            "current_status",
        ]
        # read_only_fields = ['name', 'curr_year', 'curr_sem', 'branch', 'section', 'curr_status', ]


class StudentLoginSerializer(serializers.ModelSerializer):
    roll_number = serializers.CharField(
        label="Roll Number", trim_whitespace=True, error_messages={"blank": ROLL_NUMBER_REQUIRED}
    )
    password = serializers.CharField(
        label="Password", trim_whitespace=True, error_messages={"blank": PASSWORD_REQUIRED}, write_only=True
    )

    class Meta:
        model = Student
        fields = [
            "roll_number",
            "password",
        ]

    def validate(self, data):
        roll_number = data.get("roll_number")
        password = data.get("password")
        user_obj = Student.objects.filter(roll_number__iexact=roll_number).distinct()
        if user_obj.exists() and user_obj.count() == 1:
            user_object = user_obj.first()
            user = authenticate(roll_number=user_object.roll_number, password=password)
            if user:
                data["user"] = user
            else:
                raise ValidationError({"roll_number": "Roll Number or password is incorrect"})

        return data

    def validate_roll_number(self, value):
        user_obj = Student.objects.filter(roll_number__iexact=value).distinct()
        if user_obj.exists() and user_obj.count() == 1:
            return value
        else:
            raise ValidationError("Roll Number is not registered")


class StudentSignupSerializer(serializers.ModelSerializer):
    roll_number = serializers.CharField(
        label="Roll Number",
        trim_whitespace=True,
        error_messages={"blank": ROLL_NUMBER_REQUIRED},
    )
    password = serializers.CharField(
        label="Password",
        trim_whitespace=True,
        error_messages={"blank": PASSWORD_REQUIRED},
        write_only=True,
    )
    name = serializers.CharField(read_only=True)
    token = serializers.CharField(read_only=True)
    status = serializers.CharField(label="Status", read_only=True)

    class Meta:
        model = Student
        fields = ["roll_number", "password", "status", "name", "token"]

    def create(self, validated_data):
        # try:
        roll_number = validated_data.get("roll_number")
        password = validated_data.get("password")

        user = Student.objects.filter(roll_number=roll_number)
        if user.exists():
            raise NotAcceptable({"error": USER_ALREADY_EXISTS})

        user_data = asyncio.run(login_student(roll_number, password))
        if user_data["status"] == LOGIN_SUCCESS:

            # for mapping semesters as 1,2,3,4...,8
            sems_list = []
            for sem in user_data["semesters"]:
                sems_list.append(str(sem["sem"]))

            comma_seperated_semester_list = ",".join(sems_list)

            user = Student(
                roll_number=roll_number,
                name=user_data["name"],
                current_year=user_data["current_year"],
                current_sem=user_data["current_sem"],
                branch=user_data["branch"],
                section=user_data["section"],
                current_status=user_data["current_status"],
                std_pass=password,
            )
            user.set_password(password)
            user.save()

            Signup.objects.create(
                student=user,
                logs=SignupStatusCodes.NOT_YET_STARTED.value,
                attendance_pending=comma_seperated_semester_list,
                result_pending=comma_seperated_semester_list,
            )

            token, created = Token.objects.get_or_create(user=user)

            validated_data["status"] = USER_SIGNUP_SUCCESSFUL
            validated_data["name"] = user.name
            validated_data["token"] = token
            return validated_data

        else:
            raise ValidationError({"status": user_data["status"]})
