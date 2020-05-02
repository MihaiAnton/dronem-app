"""
    @author: Badita Marin-Georgian
    @email:  geo.badita@gmail.com
    @date:   25.04.2020 20:00
"""
from django.utils.translation import gettext_lazy as _
from rest_framework import status as rest_status
from rest_framework.exceptions import APIException


class InvalidCredentialsError(APIException):
    status_code = rest_status.HTTP_400_BAD_REQUEST
    default_detail = _("Invalid credentials")
    default_code = "sign-in-error"


class ResetPasswordSendEmailError(APIException):
    status_code = rest_status.HTTP_503_SERVICE_UNAVAILABLE
    default_detail = _("Could not send reset password email")
    default_code = "email-send-error"


class ResetPasswordInvalidTokenError(APIException):
    status_code = rest_status.HTTP_400_BAD_REQUEST
    default_detail = _("Invalid token used for reset password")
    default_code = "invalid-reset-password-token"
