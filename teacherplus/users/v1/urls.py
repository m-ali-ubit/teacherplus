from django.urls import include, path
from rest_framework.routers import DefaultRouter
from teacherplus.users.v1.views import (
    UserModelViewSet,
    LoginUserAPIView,
    ForgotPasswordAPIView,
    UpdateUserPasswordAPIView,
    UserRedirectView,
)

router = DefaultRouter()
router.register(r"users", UserModelViewSet, basename="v1-users")

urlpatterns = [
    path("login/", LoginUserAPIView.as_view(), name="login"),
    path(
        "forgot_password/",
        view=ForgotPasswordAPIView.as_view(),
        name="forgot-password-email",
    ),
    path(
        "update_user_password/",
        view=UpdateUserPasswordAPIView.as_view(),
        name="update-user-password",
    ),
    path("~redirect/", view=UserRedirectView.as_view(), name="redirect"),
    path("", include(router.urls)),
]
