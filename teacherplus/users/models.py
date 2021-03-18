from teacherplus.mixins import CreateUpdateMixin
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import FileExtensionValidator
from django.db import models
from django.urls import reverse
from django_countries.fields import CountryField

from teacherplus.users.enums import UserType
from teacherplus.users.managers import (
    StudentManager,
    ParentManager,
    InstituteManager,
    TutorManager,
)


class Country(models.Model):
    country = CountryField(multiple=False, blank=True)

    def __str__(self):
        return self.country.name

    class Meta:
        verbose_name_plural = "Countries"


class City(models.Model):
    name = models.CharField(max_length=200)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Cities"


class User(AbstractUser, CreateUpdateMixin):
    class Types(models.TextChoices):
        Student = UserType.STUDENT.value, UserType.STUDENT.value.lower()
        Parent = UserType.PARENT.value, UserType.PARENT.value.lower()
        Institute = UserType.INSTITUTE.value, UserType.INSTITUTE.value.lower()
        Tutor = UserType.TUTOR.value, UserType.TUTOR.value.lower()

    base_type = Types.Student
    type = models.CharField(
        "Type", max_length=50, choices=Types.choices, default=base_type
    )

    name = models.CharField("Name", blank=True, max_length=255)
    phone = models.CharField("Phone", blank=True, max_length=50)
    city = models.ForeignKey(City, null=True, on_delete=models.CASCADE)
    address = models.CharField("Phone", blank=True, max_length=255)
    profile_image = models.FileField(
        upload_to="user/",
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=["jpg", "png", "jpeg"])],
    )

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})

    def save(self, *args, **kwargs):
        if not self.id:
            self.type = self.base_type
        return super().save(*args, **kwargs)


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    grade = models.CharField("Grade", max_length=100, blank=True)


class ParentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class InstituteProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class TutorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Student(User):
    base_type = User.Types.Student
    objects = StudentManager()

    @property
    def profile(self):
        try:
            return self.studentprofile
        except ObjectDoesNotExist:
            return None

    class Meta:
        proxy = True


class Parent(User):
    base_type = User.Types.Parent
    objects = ParentManager()

    @property
    def profile(self):
        try:
            return self.parentprofile
        except ObjectDoesNotExist:
            return None

    class Meta:
        proxy = True


class Institute(User):
    base_type = User.Types.Institute
    objects = InstituteManager()

    @property
    def profile(self):
        try:
            return self.instituteprofile
        except ObjectDoesNotExist:
            return None

    class Meta:
        proxy = True


class Tutor(User):
    base_type = User.Types.Tutor
    objects = TutorManager()

    @property
    def profile(self):
        try:
            return self.tutorprofile
        except ObjectDoesNotExist:
            return None

    class Meta:
        proxy = True
