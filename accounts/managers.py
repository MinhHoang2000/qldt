from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email=None, password=None, **kwargs):

        if not username:
            raise ValueError('User must have username')

        username = AbstractBaseUser.normalize_username(username)
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email=None, password=None, **kwargs):
        user = self.create_user(username, email, password, **kwargs)
        user.is_admin = True
        if user.is_admin is not True:
            raise ValueError('Superuser is_admin have to be True')
        user.save()
        return user
