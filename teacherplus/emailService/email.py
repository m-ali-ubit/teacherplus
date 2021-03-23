import logging

from django.core.mail import EmailMessage
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)


class EmailService:
    @classmethod
    def dispatch_email(cls, subject, email_body, recipients):
        msg = EmailMessage(from_email="admin@teacherplus.com", to=recipients)
        msg.subject = subject
        msg.body = email_body
        msg.send()

    @staticmethod
    def render_email_body(html, context):
        html_string = render_to_string(html, context)
        return html_string

    @staticmethod
    def render_and_dispatch_email(
        subject,
        recipients,
        email_template_name,
        email_context,
    ):
        email_body = EmailService.render_email_body(email_template_name, email_context)
        EmailService.dispatch_email(
            subject,
            email_body,
            recipients,
        )
