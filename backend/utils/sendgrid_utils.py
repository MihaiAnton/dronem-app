"""
    @author: Badita Marin-Georgian
    @email:  geo.badita@gmail.com
    @date:   30.04.2020 20:14
"""
import rest_framework.status as rest_status
from django.conf import settings
from django.contrib.auth import get_user_model
from python_http_client import BadRequestsError
from sendgrid import Mail
from sendgrid import SendGridAPIClient

from users.exceptions import ResetPasswordSendEmailError

User = get_user_model()


class EmailSender:
    """
    Class for sending email
    """

    @staticmethod
    def send_reset_password_email(user: User, token: str) -> None:
        message = Mail(
            from_email=settings.DEFAULT_FROM_EMAIL,
            to_emails=user.email
        )
        message.dynamic_template_data = {
            'resetLink': f'{settings.RESET_PASSWORD_DOMAIN}/reset-password/{token}',
            'firstName': user.username,
            'subject': 'Reset Password'
        }

        message.template_id = settings.EMAIL_TEMPLATE_IDS['password-reset']
        try:
            response = SendGridAPIClient(settings.SENDGRID_API_KEY).send(message)
            if response.status_code != rest_status.HTTP_202_ACCEPTED:
                raise ResetPasswordSendEmailError()
        except BadRequestsError:
            raise ResetPasswordSendEmailError()
