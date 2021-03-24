from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model

from teacherplus.mixins import ReadOnlyDateMixin
from teacherplus.users.forms import UserChangeForm, UserCreationForm
from teacherplus.users.models import (
    Student,
    Parent,
    Institute,
    Teacher,
    StudentProfile,
    ParentProfile,
    InstituteProfile,
    TeacherProfile,
    TeacherEducation,
    StudentEducation,
    Experience,
    TeachingExperience,
)

User = get_user_model()


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):

    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = (("User", {"fields": ("name",)}),) + auth_admin.UserAdmin.fieldsets
    list_display = ["username", "name", "is_superuser"]
    search_fields = ["name"]


class StudentAdmin(ReadOnlyDateMixin):
    list_display = ["id", "name"]


class ParentAdmin(ReadOnlyDateMixin):
    list_display = ["id", "name"]


class InstituteAdmin(ReadOnlyDateMixin):
    list_display = ["id", "name"]


class TeacherAdmin(ReadOnlyDateMixin):
    list_display = ["id", "name"]


class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ["id", "user"]


class ParentProfileAdmin(admin.ModelAdmin):
    list_display = ["id", "user"]


class InstituteProfileAdmin(admin.ModelAdmin):
    list_display = ["id", "user"]


class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = ["id", "user"]


class TeacherEducationAdmin(ReadOnlyDateMixin):
    list_display = ["id", "profile"]


class StudentEducationAdmin(ReadOnlyDateMixin):
    list_display = ["id", "profile"]


class ExperienceAdmin(ReadOnlyDateMixin):
    list_display = ["id", "profile"]


class TeachingExperienceAdmin(ReadOnlyDateMixin):
    list_display = ["id", "profile"]


admin.site.register(Student, StudentAdmin)
admin.site.register(Parent, ParentAdmin)
admin.site.register(Institute, InstituteAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(StudentProfile, StudentProfileAdmin)
admin.site.register(ParentProfile, ParentProfileAdmin)
admin.site.register(InstituteProfile, InstituteProfileAdmin)
admin.site.register(TeacherProfile, TeacherProfileAdmin)
admin.site.register(TeacherEducation, TeacherEducationAdmin)
admin.site.register(StudentEducation, StudentEducationAdmin)
admin.site.register(Experience, ExperienceAdmin)
admin.site.register(TeachingExperience, TeachingExperienceAdmin)
