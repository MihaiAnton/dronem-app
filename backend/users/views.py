import secrets
from datetime import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout
from rest_framework import exceptions as rest_exceptions
from rest_framework import generics as rest_generics
from rest_framework import permissions as rest_permissions
from rest_framework import status as rest_status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from users.exceptions import InvalidCredentialsError
from users.exceptions import ResetPasswordInvalidTokenError
from users.models import PasswordResetRequest
from users.serializers import PasswordRequestResetSerializer
from users.serializers import PasswordResetConfirmationSerializer
from users.serializers import SignInSerializer
from users.serializers import SignOutSerializer
from users.serializers import SignUpSerializer
from utils.sendgrid_utils import EmailSender

User = get_user_model()


class SignUpView(rest_generics.CreateAPIView):
    permission_classes = (rest_permissions.AllowAny,)
    serializer_class = SignUpSerializer

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        return Response(status=rest_status.HTTP_201_CREATED)


class SignInView(rest_generics.CreateAPIView):
    serializer_class = SignInSerializer
    permission_classes = (rest_permissions.AllowAny,)
    authentication_classes = (TokenAuthentication,)

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            django_login(request, user)
            return Response(status=rest_status.HTTP_201_CREATED, data={'token': token.key})
        except rest_exceptions.ValidationError:
            raise InvalidCredentialsError


class SignOutView(rest_generics.CreateAPIView):
    permission_classes = (rest_permissions.IsAuthenticated,)
    serializer_class = SignOutSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        request_token = serializer.validated_data.get('token')
        Token.objects.filter(key=request_token).delete()
        django_logout(request)
        return Response(status=rest_status.HTTP_200_OK)


class PasswordResetRequestCreateView(rest_generics.CreateAPIView):
    serializer_class = PasswordRequestResetSerializer
    permission_classes = (rest_permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['token'] = secrets.token_urlsafe(64)
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        return Response(status=rest_status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        email = serializer.validated_data['email']

        try:
            user = User.objects.get(email=email)
            serializer.save()
            EmailSender.send_reset_password_email(
                user,
                serializer.initial_data['token']
            )
        except User.DoesNotExist:
            pass


class PasswordResetRequestRetrieveView(rest_generics.RetrieveAPIView):
    serializer_class = PasswordRequestResetSerializer
    permission_classes = (rest_permissions.AllowAny,)

    def get_object(self):
        try:
            return PasswordResetRequest.objects.retrieve_by_token(self.kwargs['token'])
        except PasswordResetRequest.DoesNotExist:
            raise ResetPasswordInvalidTokenError


# TODO TESTS
class PasswordResetConfirmationView(rest_generics.CreateAPIView):
    serializer_class = PasswordResetConfirmationSerializer
    permission_classes = (rest_permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        return Response(status=rest_status.HTTP_200_OK)

    def perform_create(self, serializer):
        token = serializer.initial_data.get('token')
        new_password = serializer.initial_data.get('new_password')
        try:
            password_request = PasswordResetRequest.objects.retrieve_by_token(token)
            PasswordResetRequest.objects.filter(email=password_request.email, can_be_used=True).update(
                can_be_used=False
            )
            user = User.objects.get(email=password_request.email)
            user.set_password(new_password)
            user.save()
        except PasswordResetRequest.DoesNotExist:
            raise ResetPasswordInvalidTokenError
        # TODO add an successful password changed
