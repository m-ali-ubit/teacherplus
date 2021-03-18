import logging

from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.views.generic import RedirectView
from rest_framework import status, permissions
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from teacherplus.users.email import UserEmail
from teacherplus.users.enums import UserType
from teacherplus.users.helpers import UpdatePasswordHelper
from teacherplus.users.v1.serializers import (
    UserSerializer,
    ForgotPasswordEmailSerializer,
    UpdatePasswordRequestSerializer,
    LoginRequestSerializer, StudentSerializer,
)
from teacherplus.utils.permissions import UpdatePasswordPermission
from teacherplus.utils.response_handler import validation_exception_handler

logger = logging.getLogger(__name__)

User = get_user_model()

user_type_serializer_mapper = {
    UserType.STUDENT.value: StudentSerializer,
    # UserType.PARENT.value: ParentSerializer,
    # UserType.INSTITUTE.value: InstituteSerializer,
    # UserType.TUTOR.value: TutotSerializer,
}


class UserViewSet(ViewSet):

    @action(methods=["POST"], detail=False)
    # def tuto

    def get_serializer_class(self):
        user_type = self.request.data.get("type")
        assert user_type is not None and user_type in UserType.get_user_types(), (
            f"Either 'type' key is missing in request or has invalid user type. "
            f"Available user types are {UserType.get_user_types()}"
        )
        return user_type_serializer_mapper[user_type]


class UserRedirectView(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})


class ForgotPasswordAPIView(APIView):
    def validate_email(self, query_params):
        serializer = ForgotPasswordEmailSerializer(data=query_params)
        serializer.is_valid(raise_exception=True)
        return serializer.validated_data.get("email")

    def get(self, request) -> Response:
        try:
            user_email_address = self.validate_email(request.query_params)
            user = get_object_or_404(User, email=user_email_address)
            url = request.build_absolute_uri("/")[:-1]
            UserEmail.send_password_update_email(
                user, UpdatePasswordHelper.generate_update_password_url(user, url)
            )
        except Http404:
            logger.error(
                f"Failure to find the object, the User with the email "
                f"{user_email_address} doesnt exist"
            )
            return Response(
                data=f"The User with the email {user_email_address} doesnt exist.",
                status=status.HTTP_400_BAD_REQUEST,
            )
        except ValidationError as validation_error:
            logger.error(
                f"Validation error occurred while sending forget password email. "
                f"Error: {validation_error}"
            )
            return Response(
                data="The email address is not valid",
                status=status.HTTP_400_BAD_REQUEST,
            )
        logger.info(
            f"Email for updating password has been sent to {user_email_address}"
        )
        return Response(
            data="Email has been sent successfully", status=status.HTTP_200_OK
        )


class UpdateUserPasswordAPIView(APIView):
    permission_classes = [UpdatePasswordPermission]

    def get_permissions(self):
        if self.request.data.get("is_admin"):
            return [permissions.IsAuthenticated()]
        return super(UpdateUserPasswordAPIView, self).get_permissions()

    def post(self, request) -> Response:
        try:
            serialized_data = UpdatePasswordRequestSerializer(data=request.data)
            serialized_data.is_valid(raise_exception=True)
            user = get_object_or_404(User, email=request.data.get("email"))
            user.set_password(serialized_data.data["confirm_password"])
            user.save()
            UpdatePasswordHelper.invalidate_update_password_token(user.email)
            return Response(
                data="Password has been updated successfully", status=status.HTTP_200_OK
            )
        except Http404:
            logger.error(f"Failure to find the object, user with email doesnt exist")
            return Response(
                data="The User doesn't exist", status=status.HTTP_400_BAD_REQUEST
            )
        except ValidationError as validation_error:
            logger.error(
                f"Validation error occurred while updating the password with {validation_error}"
            )
            return Response(
                data=f"Failed to update the password with {validation_error}",
                status=status.HTTP_400_BAD_REQUEST,
            )


class LoginUserAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        try:
            request_serializer = LoginRequestSerializer(data=request.data)
            request_serializer.is_valid(raise_exception=True)
            username = request_serializer.validated_data.get("username")
            email = request_serializer.validated_data.get("email")
            password = request_serializer.validated_data["password"]

            user = authenticate(username=username, email=email, password=password)

            if not user:
                return Response(
                    data="Credentials not correct. Unable to Login.",
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            refresh_token = RefreshToken.for_user(user)
            return Response(
                data={
                    "token": str(refresh_token.access_token),
                    "refresh": str(refresh_token),
                    "user": UserSerializer(user).data,
                    "message": "Successfully logged in.",
                },
                status=status.HTTP_200_OK,
            )

        except ValidationError as error:
            logger.info(f"Validation failed for User Login with exception {error}")
            data = validation_exception_handler(error)
            data.update({"message": error.default_detail})
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
