from django.urls import path, include

app_name = "users"
urlpatterns = [path("v1/users/", include("teacherplus.users.v1.urls"))]
