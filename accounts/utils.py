from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.hashers import make_password

import requests

class UserManager(BaseUserManager):
    def create_user(self, username, password, is_staff=False, **fields):
        if not username:
            raise ValueError('Used username is null.')
        
        if not password:
            raise ValueError('User password is null.')
        
        uuid = requests.get(f'https://api.mojang.com/users/profiles/minecraft/{username}').json()['id']

        user = self.model(username=username, password=make_password(password), is_staff=is_staff, uuid=uuid, **fields)
        user.save()
        return user