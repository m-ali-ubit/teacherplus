from django.urls import path, include

app_name = "users"
urlpatterns = [path("v1/", include("teacherplus.users.v1.urls"))]
