from django.urls import path, include

app_name = "posts"
urlpatterns = [path("v1/", include("teacherplus.posts.v1.urls"))]
