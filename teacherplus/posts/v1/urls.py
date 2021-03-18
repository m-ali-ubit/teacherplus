from django.urls import path, include
from rest_framework.routers import DefaultRouter

from teacherplus.posts.v1.views import ActivityView, PostView

app_name = "posts"

router = DefaultRouter()

router.register(r"activity_log/", ActivityView, basename="v1-activity-log")
router.register(r"posts/", PostView, basename="v1-posts")

urlpatterns = [
    path("", include(router.urls)),
]
