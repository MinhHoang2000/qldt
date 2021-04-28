from .serializers import AccountSerializer
import logging
logger = logging.getLogger(__name__)


def create_account(account_data, is_admin=False):
    account_serializer = AccountSerializer(data=account_data, context={'is_admin': is_admin})
    account_serializer.is_valid(raise_exception=True)
    return account_serializer.save()


def update_account(account, account_data):
    account_serializer = AccountSerializer(account, data=account_data, partial=True)
    account_serializer.is_valid(raise_exception=True)
    account_serializer.save()
