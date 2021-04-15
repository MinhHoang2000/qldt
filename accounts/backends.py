from django.contrib.auth.backends import BaseBackend
from .models import Account


class CustomBackend(BaseBackend):
    def authenticate(self, request, **kwargs):
        username = kwargs['username']
        password = kwargs['password']

        try:
            user = Account.objects.get(username=username)
            if user.check_password(password):
                return user
            else:
                return None
        except Account.DoesNotExsit:
            pass

        return None

    def get_user(self, user_id):
        try:
            return Account.objects.get(pk=user_id)
        except Account.DoesNotExist:
            return None

    def get_user_permissions(self, user_obj, obj=None):
        if not user_obj.is_active or user_obj.is_anonymous:
            return set()

        perms = user_obj.permissions.all().value_list()
        perms = ["{code}" for id, name, code in perms]

        return perms
