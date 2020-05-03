"""
    @author: Badita Marin-Georgian
    @email:  geo.badita@gmail.com
    @date:   25.04.2020 19:04
"""
import re

from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import serializers as rest_serializers
from validate_email import validate_email

User = get_user_model()


def generic_username_validator(username: str):
    """
    Checks if username respects the requirements
    """

    if len(username) < settings.USERNAME_MIN_LENGTH:
        raise rest_serializers.ValidationError(f"Username must have at least {settings.USERNAME_MIN_LENGTH} characters")
    if len(username) > settings.USERNAME_MAX_LENGTH:
        raise rest_serializers.ValidationError(f"Username must have at most {settings.USERNAME_MAX_LENGTH} characters")

    if not username[0].isalpha():
        raise rest_serializers.ValidationError("Username must start with an alphanumeric character")

    if not re.match(settings.USERNAME_REGEX, username):
        raise rest_serializers.ValidationError("Username contains invalid characters")


def not_email_validator(username: str):
    """
    Check if username has email format
    """
    is_email = validate_email(email_address=username, check_regex=True, check_mx=False, use_blacklist=False)

    if is_email:
        raise rest_serializers.ValidationError("You cannot user an email address as username")


def password_strength_validator(password: str):
    """
    Check if a given password is stong enough
    """

    if len(password) < settings.MIN_PASSWORD_LENGTH:
        raise rest_serializers.ValidationError("Password is too short")


def password_contains_username_validator(password: str, username: str):
    """
    Check if a password contains username
    """
    if password in username:
        raise rest_serializers.ValidationError("Password can't contain username")


def unique_username_validator(username: str):
    """
    Check if a username is unique
    """
    if User.objects.filter(username=username).exists():
        raise rest_serializers.ValidationError("Username must be unique")


def unique_email(email: str):
    """
    Check if an email is unique
    """
    if User.objects.filter(email=email).exists():
        raise rest_serializers.ValidationError("Email must be unique")


username_validators = [generic_username_validator, not_email_validator, unique_username_validator]
password_validators = [password_strength_validator]
email_validators = [unique_email]
