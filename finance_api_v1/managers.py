from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.hashers import make_password

import requests, random


class FinanceProfileManager(BaseUserManager):

    def __generate_uuid(self):
        uuid = random.randint(1000000, 9999999)
        if self.model.objects.filter(title=uuid).exists():
            return self.__generate_uuid()
        else:
            return uuid

    def get_profile(self, user):
        if not self.model.objects.filter(user=user).exists():
            profile = self.model()
            profile.user = user
            if user.username is not None:
                profile.title = user.username
            else:
                profile.title = str(self.__generate_uuid())
            profile.save()
        else:
            profile = self.model.objects.get(user=user)
        return profile