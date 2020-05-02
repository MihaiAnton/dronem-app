"""
    @author: Badita Marin-Georgian
    @email:  geo.badita@gmail.com
    @date:   25.04.2020 19:01
"""

from django.contrib.auth import authenticate as django_authenticate
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers as rest_serializers

from users.models import PasswordResetRequest
from users.validators import email_validators
from users.validators import password_contains_username_validator
from users.validators import password_validators
from users.validators import username_validators
from utils.token_utils import hash_token

User = get_user_model()


class SignUpSerializer(rest_serializers.ModelSerializer):
    username = rest_serializers.CharField(max_length=255, required=True, validators=username_validators)
    password = rest_serializers.CharField(max_length=255, required=True, validators=password_validators)
    email = rest_serializers.EmailField(max_length=255, required=True, validators=email_validators)

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)

    def save(self):
        instance = super().save()
        instance.set_password(self.validated_data.get('password'))
        return instance.save()


class SignInSerializer(rest_serializers.Serializer):
    username = rest_serializers.CharField(max_length=255, required=True)
    password = rest_serializers.CharField(max_length=255, required=True)

    def validate_password(self, value):
        password_contains_username_validator(value, self.initial_data['username'])
        return value

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = django_authenticate(request=self.context.get('request'),
                                       username=username, password=password)

            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise rest_serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "username" and "password".')
            raise rest_serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class SignOutSerializer(rest_serializers.Serializer):
    token = rest_serializers.CharField(max_length=255, required=True)


class PasswordTokenField(rest_serializers.CharField):
    def to_internal_value(self, data):
        value = super().to_internal_value(data)
        value = hash_token(value)
        return value


class PasswordRequestResetSerializer(rest_serializers.ModelSerializer):
    email = rest_serializers.EmailField(max_length=255, write_only=True, required=True)
    token = PasswordTokenField(max_length=255)
    is_valid = rest_serializers.SerializerMethodField()

    class Meta:
        model = PasswordResetRequest
        fields = ('email', 'token', 'is_valid',)

    def get_is_valid(self, instance):
        return instance.is_valid


class PasswordResetConfirmationSerializer(rest_serializers.Serializer):
    token = PasswordTokenField(max_length=255, required=True)
    new_password = rest_serializers.CharField(max_length=255, required=True, validators=password_validators)

    def validate_token(self, value):
        try:
            token = self.initial_data['token']
            pass_request = PasswordResetRequest.objects.retrieve_by_token(token)
            if not pass_request.is_valid:
                raise rest_serializers.ValidationError(
                    "Invalid password reset request"
                )
        except PasswordResetRequest.DoesNotExist:
            raise rest_serializers.ValidationError(
                "There is no request with the given token"
            )

        return value
