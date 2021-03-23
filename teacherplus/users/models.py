from datetime import datetime

from teacherplus.mixins import CreateUpdateMixin
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import FileExtensionValidator
from multiselectfield import MultiSelectField
from django.db import models
from django.urls import reverse

from teacherplus.users.constants import (
    EmploymentType,
    JobType,
    UserType,
    Gender,
    Shifts,
    Availability,
    COURSES,
)
from teacherplus.users.managers import (
    StudentManager,
    ParentManager,
    InstituteManager,
    TeacherManager,
)
from teacherplus.utils.models import City


class User(AbstractUser, CreateUpdateMixin):

    base_type = UserType.STUDENT
    user_type = models.CharField(
        "User Type", max_length=50, choices=UserType.choices, default=base_type
    )

    name = models.CharField("Name", blank=True, max_length=255)
    phone = models.CharField("Phone", blank=True, max_length=50)
    city = models.ForeignKey(City, null=True, on_delete=models.CASCADE)
    address = models.CharField("Address", blank=True, max_length=255)
    gender = models.CharField(
        "Gender", choices=Gender.choices, default=Gender.MALE, max_length=6
    )
    date_of_birth = models.DateField("Date of birth", null=True, blank=True)
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
            self.user_type = self.base_type
        return super().save(*args, **kwargs)


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    grade = models.CharField("Grade", max_length=100, blank=True)


class ParentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class InstituteProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class TeacherProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    shifts = MultiSelectField(max_choices=2, choices=Shifts.choices)
    job_types = MultiSelectField(max_choices=2, choices=JobType.choices)
    availabilities = MultiSelectField(max_choices=4, choices=Availability.choices)
    cnic = models.CharField("CNIC", max_length=50, null=True)
    description = models.TextField("Description", null=True, blank=True)
    intro_link = models.URLField("Introduction Video Link", null=True, blank=True)
    demo_link = models.URLField("Demo Video Link", null=True, blank=True)


class Student(User):
    base_type = UserType.STUDENT
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
    base_type = UserType.PARENT
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
    base_type = UserType.INSTITUTE
    objects = InstituteManager()

    @property
    def profile(self):
        try:
            return self.instituteprofile
        except ObjectDoesNotExist:
            return None

    class Meta:
        proxy = True


class Teacher(User):
    base_type = UserType.TEACHER
    objects = TeacherManager()

    @property
    def profile(self):
        try:
            return self.teacherprofile
        except ObjectDoesNotExist:
            return None

    class Meta:
        proxy = True


class BaseEducation(CreateUpdateMixin):
    school = models.CharField("School", max_length=200)
    degree = models.CharField("Degree", max_length=100)
    field = models.CharField("Field of study", max_length=100, null=True, blank=True)
    start_year = models.DateField("Start Year")
    end_year = models.DateField("End Year")
    grade = models.CharField("Grade", max_length=10, null=True, blank=True)
    activities = models.TextField("Activities", null=True, blank=True)

    @property
    def duration(self):
        return self.end_year - self.start_year

    class Meta:
        abstract = True


class TeacherEducation(BaseEducation):
    profile = models.ForeignKey(
        "TeacherProfile",
        related_name="education",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )


class StudentEducation(BaseEducation):
    profile = models.ForeignKey(
        "StudentProfile",
        related_name="education",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )


class BaseExperience(CreateUpdateMixin):
    title = models.CharField("Title", max_length=100)
    location = models.CharField("Location", max_length=100, null=True, blank=True)
    start_year = models.DateField("Start Year")
    end_year = models.DateField("End Year", null=True, blank=True)
    description = models.TextField("Description", null=True, blank=True)

    @property
    def duration(self):
        end_year = self.end_year or datetime.now().date()
        return end_year - self.start_year

    class Meta:
        abstract = True


class Experience(BaseExperience):
    employment_type = models.CharField(
        "Employment Type", max_length=15, choices=EmploymentType.choices
    )
    company = models.CharField("Company", max_length=100)
    profile = models.ForeignKey(
        "TeacherProfile",
        related_name="experience",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )


class TeachingExperience(BaseExperience):
    job_type = models.CharField("Job Type", max_length=15, choices=JobType.choices)
    institute = models.CharField("Institute", max_length=100, null=True, blank=True)
    subject = MultiSelectField("Courses", choices=COURSES)
    class_grade = models.CharField("Class/Grade", max_length=150, null=True, blank=True)
    profile = models.ForeignKey(
        "TeacherProfile",
        related_name="teaching_experience",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
