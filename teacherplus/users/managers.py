from django.db import models

from teacherplus.users.constants import UserType


class StudentManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(user_type=UserType.STUDENT)


class ParentManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(user_type=UserType.PARENT)


class InstituteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(user_type=UserType.INSTITUTE)


class TeacherManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(user_type=UserType.TEACHER)
