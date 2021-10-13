import jwt

from datetime import datetime
from datetime import timedelta

from django.conf import settings
from django.db import models
import time

from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin

from .utils import UserManager

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(db_index=True, max_length=16, unique=True, null=True, blank=True)

    verification = models.CharField(max_length=8, default="full")

    email = models.CharField(db_index=True, max_length=254, unique=True, null=True)

    password = models.CharField(max_length=256, default='')

    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ()

    objects = UserManager()

    def __str__(self):
        return self.email

    def check_role(self, name):
        if self.groups.filter(name=name).exists():
            return True
        elif self.groups.filter(name="administrator").exists():
            return True
        else:
            return False

    @property
    def token(self, days=30):
        return self._generate_jwt_token(days=days)

    def _generate_jwt_token(self, days):
        token = jwt.encode({
            'id': self.pk,
            'exp': time.time() + 60 * 60 * 60 * 24 * days
        }, settings.SECRET_KEY, algorithm='HS256')
        return token
