import uuid

from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email
from rest_framework import serializers

from teacherplus.users.constants import Gender, Shifts, JobType, Availability
from teacherplus.users.models import (
    User,
    Teacher,
    TeacherProfile,
)
from teacherplus.users.v1.serializers.model_serializer import (
    CitySerializer,
    ExperienceSerializer,
    TeachingExperienceSerializer, TeacherEducationSerializer,
)
from teacherplus.utils.validations import validate_existing_email


def get_user_data_by_email(email):
    user = User.objects.get(email=email)
    user_data = UserPasswordValidationSerializer(user).data
    return user_data


class StudentRequestSerializer(serializers.Serializer):
    pass


class ParentRequestSerializer(serializers.Serializer):
    pass


class InstituteRequestSerializer(serializers.Serializer):
    pass


class TeacherRequestSerializer(serializers.Serializer):
    name = serializers.CharField(required=True)
    email = serializers.EmailField(validators=[validate_email, validate_existing_email])
    password = serializers.CharField(required=True)
    phone = serializers.CharField(required=False)
    city = CitySerializer(required=True)
    address = serializers.CharField(required=False)
    gender = serializers.ChoiceField(choices=Gender.choices, required=True)
    date_of_birth = serializers.DateField(required=False)
    profile_image = serializers.FileField(required=False)
    shifts = serializers.MultipleChoiceField(choices=Shifts.choices, required=False)
    job_types = serializers.MultipleChoiceField(choices=JobType.choices, required=False)
    availabilities = serializers.MultipleChoiceField(
        choices=Availability.choices, required=False
    )
    cnic = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    intro_link = serializers.URLField(required=False)
    demo_link = serializers.URLField(required=False)
    education = TeacherEducationSerializer(many=True, required=False)
    experience = ExperienceSerializer(many=True, required=False)
    teaching_experience = TeachingExperienceSerializer(many=True, required=False)

    @staticmethod
    def validate_password(value):
        validate_password(value)
        return value

    @staticmethod
    def get_username(email):
        return f"{email.split('@')[0]}{uuid.uuid4().hex[:6]}"

    def create(self, validated_data):
        username = self.get_username(validated_data["email"])
        # Creating Teacher user object
        teacher = Teacher.objects.create(
            username=username,
            email=validated_data.pop("email"),
            phone=validated_data.pop("phone", ""),
            city=validated_data.pop("city", None),
            address=validated_data.pop("address", ""),
            gender=validated_data.pop("gender"),
            date_of_birth=validated_data.pop("date_of_birth", None),
            profile_image=validated_data.pop("profile_image", None),
        )
        teacher.set_password(validated_data["password"])
        teacher.save()
        # Creating Teacher profile object and attaching it with its user object
        TeacherProfile.objects.create(user=teacher, **validated_data)
        return teacher


class ForgotPasswordEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()


class UserPasswordValidationSerializer(serializers.Serializer):
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.CharField(validators=[validate_email, validate_existing_email])

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email")


class UpdatePasswordRequestSerializer(serializers.Serializer):
    password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    def validate_password(self, value):
        user = get_user_data_by_email(self.initial_data.get("email"))
        validate_password(value, user)
        return value

    def validate(self, attrs):
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError(
                "Password and Confirmed password should be equal"
            )
        return attrs


class LoginRequestSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    remember_me = serializers.BooleanField(default=False)
