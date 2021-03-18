from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email
from rest_framework import serializers

from teacherplus.users.models import User, StudentProfile, Student
from teacherplus.utils.validations import validate_existing_email


def get_user_data_by_email(email):
    user = User.objects.get(email=email)
    user_data = UserPasswordValidationSerializer(user).data
    return user_data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "name",
            "first_name",
            "last_name",
            "profile_image",
            "url",
        )

        extra_kwargs = {
            "url": {"view_name": "v1:user-detail", "lookup_field": "username"}
        }


class StudentSerializer(serializers.ModelSerializer):
    grade = serializers.CharField(source="profile.grade")

    class Meta:
        model = Student
        fields = (
            "id",
            "username",
            "email",
            "name",
            "first_name",
            "last_name",
            "grade",
        )


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
