import json
from django.db import models

from teacherplus.users.enums import (
    UserTypeEnum,
    GenderEnum,
    ShiftsEnum,
    JobTypeEnum,
    AvailabilityEnum,
    EmploymentTypeEnum,
)


class UserType(models.TextChoices):
    STUDENT = UserTypeEnum.STUDENT.value, UserTypeEnum.STUDENT.value.lower()
    PARENT = UserTypeEnum.PARENT.value, UserTypeEnum.PARENT.value.lower()
    INSTITUTE = UserTypeEnum.INSTITUTE.value, UserTypeEnum.INSTITUTE.value.lower()
    TEACHER = UserTypeEnum.TEACHER.value, UserTypeEnum.TEACHER.value.lower()


class Gender(models.TextChoices):
    MALE = GenderEnum.MALE.value, GenderEnum.MALE.value.lower()
    FEMALE = GenderEnum.FEMALE.value, GenderEnum.FEMALE.value.lower()


class Shifts(models.TextChoices):
    MORNING = ShiftsEnum.MORNING.value, ShiftsEnum.MORNING.value.lower()
    EVENING = ShiftsEnum.EVENING.value, ShiftsEnum.EVENING.value.lower()


class JobType(models.TextChoices):
    PART_TIME = JobTypeEnum.PART_TIME.value, JobTypeEnum.PART_TIME.value.lower()
    FULL_TIME = JobTypeEnum.FULL_TIME.value, JobTypeEnum.FULL_TIME.value.lower()


class Availability(models.TextChoices):
    PRIVATE = AvailabilityEnum.PRIVATE.value, AvailabilityEnum.PRIVATE.value.lower()
    GROUP = AvailabilityEnum.GROUP.value, AvailabilityEnum.GROUP.value.lower()
    ONLINE = AvailabilityEnum.ONLINE.value, AvailabilityEnum.ONLINE.value.lower()
    CENTRE = AvailabilityEnum.CENTRE.value, AvailabilityEnum.CENTRE.value.lower()


class EmploymentType(models.TextChoices):
    PART_TIME = (
        EmploymentTypeEnum.PART_TIME.value,
        EmploymentTypeEnum.PART_TIME.value.lower(),
    )
    FULL_TIME = (
        EmploymentTypeEnum.FULL_TIME.value,
        EmploymentTypeEnum.FULL_TIME.value.lower(),
    )
    SELF_EMPLOYED = (
        EmploymentTypeEnum.SELF_EMPLOYED.value,
        EmploymentTypeEnum.SELF_EMPLOYED.value.lower(),
    )
    FREELANCE = (
        EmploymentTypeEnum.FREELANCE.value,
        EmploymentTypeEnum.FREELANCE.value.lower(),
    )
    INTERNSHIP = (
        EmploymentTypeEnum.INTERNSHIP.value,
        EmploymentTypeEnum.INTERNSHIP.value.lower(),
    )


with open("teacherplus/users/data/courses.json", "r") as f:
    courses = json.loads(f.read())

COURSES = list(courses.items())
