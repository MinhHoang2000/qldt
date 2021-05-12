from .serializers import AccountSerializer
from django.contrib.auth import get_user_model
from rest_framework import exceptions


def get_account(id):
    try:
        return get_user_model().objects.get(id=id)
    except get_user_model().DoesNotExist:
        raise exceptions.NotFound("Account does not exist")


def create_account(account_data, is_admin=False):
    account_serializer = AccountSerializer(data=account_data, context={'is_admin': is_admin})
    account_serializer.is_valid(raise_exception=True)
    return account_serializer.save()


def update_account(account, account_data):
    account_serializer = AccountSerializer(account, data=account_data, partial=True)
    account_serializer.is_valid(raise_exception=True)
    account_serializer.save()


def delete_account(id):
    return get_account(id).delete()
