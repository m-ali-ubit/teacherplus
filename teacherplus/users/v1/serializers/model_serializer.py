from rest_framework import serializers

from teacherplus.users.constants import Shifts, Availability, JobType
from teacherplus.users.models import (
    User,
    Student,
    Parent,
    Institute,
    Teacher,
    Experience,
    TeachingExperience,
    TeacherEducation,
    StudentEducation,
)
from teacherplus.utils.models import City


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "name",
            "first_name",
            "last_name",
            "profile_image",
            "url",
        )

        extra_kwargs = {
            "url": {"view_name": "v1:user-detail", "lookup_field": "username"}
        }


class StudentSerializer(serializers.ModelSerializer):
    grade = serializers.CharField(source="profile.grade")

    class Meta:
        model = Student
        fields = (
            "id",
            "username",
            "email",
            "name",
            "first_name",
            "last_name",
            "grade",
        )


class ParentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parent
        fields = "__all__"


class InstituteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institute
        fields = "__all__"


class TeacherEducationSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = TeacherEducation


class StudentEducationSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = StudentEducation


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = City


class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Experience


class TeachingExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = TeachingExperience


class TeacherSerializer(serializers.ModelSerializer):
    shifts = serializers.MultipleChoiceField(
        source="profile.shifts", choices=Shifts.choices
    )
    job_types = serializers.MultipleChoiceField(
        source="profile.job_types", choices=JobType.choices
    )
    availabilities = serializers.MultipleChoiceField(
        source="profile.availabilities", choices=Availability.choices
    )
    cnic = serializers.CharField(source="profile.cnic")
    description = serializers.CharField(source="profile.description")
    intro_link = serializers.URLField(source="profile.intro_link")
    demo_link = serializers.URLField(source="profile.demo_link")
    education = TeacherEducationSerializer(source="profile.education", many=True)
    experience = ExperienceSerializer(source="profile.experience", many=True)
    teaching_experience = TeachingExperienceSerializer(
        source="profile.teaching_experience", many=True
    )

    class Meta:
        model = Teacher
        fields = (
            "id",
            "name",
            "email",
            "username",
            "phone",
            "address",
            "gender",
            "cnic",
            "description",
            "intro_link",
            "demo_link",
            "date_of_birth",
            "created_at",
            "shifts",
            "job_types",
            "availabilities",
            "education",
            "experience",
            "teaching_experience",
            "created_at",
        )
