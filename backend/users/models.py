"""
    @author: Badita Marin-Georgian
    @email:  geo.badita@gmail.com
    @date:   30.04.2020 20:46
"""
from datetime import datetime

import pytz
from django.conf import settings
from django.db import models

from utils.token_utils import check_token


class PasswordResetRequestManager(models.Manager):
    def retrieve_by_token(self, token: str) -> models.Model:
        for request in self.filter(can_be_used=True).order_by('-created_at'):
            if check_token(token, request.token):
                return request

        raise self.model.DoesNotExist(
            f'{self.model._meta.object_name} matching query does not exist.'
        )


class PasswordResetRequest(models.Model):
    email = models.EmailField(max_length=255)
    token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now=True)
    can_be_used = models.BooleanField(default=True)

    objects = PasswordResetRequestManager()

    def __str__(self):
        return f'{self.email} - {self.token} - {self.created_at} - {self.can_be_used}'

    @property
    def is_valid(self):
        now = datetime.now().replace(tzinfo=pytz.UTC)
        created_at = self.created_at.replace(tzinfo=pytz.UTC)
        return self.can_be_used and now >= created_at and (
                now - created_at).seconds <= settings.PASSWORD_RESET_TIMEOUT_SECONDS
