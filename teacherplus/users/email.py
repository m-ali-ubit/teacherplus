from teacherplus.emailService.email import EmailService


class UserEmail:
    @staticmethod
    def send_password_update_email(user, update_password_link):
        subject = "Reset Password"
        context = {"user_name": user.name, "reset_password_link": update_password_link}
        EmailService.render_and_dispatch_email(
            subject, user.email, "reset_password.html", context
        )
