from django.contrib.auth import get_user_model
from django.utils.translation import ugettext as _
from rest_framework.exceptions import ValidationError

User = get_user_model()


def validate_existing_email(email):
    user = User.objects.filter(email=email.lower())
    if not user:
        return email
    raise ValidationError("This email address is already registered to an account.")


class AlphabeticPasswordValidator:
    def validate(self, password, user=None):
        if password.isalpha():
            raise ValidationError(
                _("Your password should be a combination of alphanumeric characters."),
                code="password_entirely_alphabetic",
            )

    def get_help_text(self):
        return _("Your password should be a combination of alphanumeric characters.")


class UpperCaseLetterPasswordValidator:
    def validate(self, password, user=None):
        if not any(x.isupper() for x in password):
            raise ValidationError(
                _(
                    "Password should be a combination of uppercase and lowercase letter."
                ),
                code="password_entirely_lower_case",
            )

    def get_help_text(self):
        return _("Password should be a combination of uppercase and lowercase letter.")
