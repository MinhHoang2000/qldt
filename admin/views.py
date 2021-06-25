from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from rest_framework import status, serializers
from rest_framework.response import Response

from .serializers import *
from config.pagination import Pagination, PaginationHandlerMixin

from accounts.models import Permission
from django.contrib.auth import get_user_model

from accounts.serializers import AccountSerializer, PermissionSerializer

from accounts.utils import create_account, update_account, delete_account, delete_permission

from .students import *
from .teachers import *
from .achievements import *
from .classrooms import *
from .school import *
from .schema import *

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

import logging
logger = logging.getLogger(__name__)


# Account

class ListAccountView(APIView, PaginationHandlerMixin):
    # permission_classes = (IsAdminUser, IsAuthenticated)
    pagination_class = Pagination

    def get(self, request):
        accounts = get_user_model().objects.all()

        username = request.query_params.get('username')
        id = request.query_params.get('id')
        sort = request.query_params.get('sort_by')

        if username:
            accounts = accounts.filter(username=username)
        if id:
            accounts = accounts.filter(id=id)
        if sort:
            accounts = accounts.order_by(f'{sort}')

        serializer = AccountSerializer(accounts, many=True)
        page = self.paginate_queryset(accounts)
        if page is not None:
            serializer = self.get_paginated_response(AccountSerializer(page, many=True).data)

        return Response(serializer.data, status=status.HTTP_200_OK)

class RegisterView(APIView):
    # permission_classes = (IsAuthenticated, IsAdminUser)

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties=SIGNUP_ACCOUNT_PROP,
        required = SIGNUP_ACCOUNT_REQUIRED))
    def post(self, request):
        is_admin = request.data.get('is_admin', False)
        account = create_account(request.data, is_admin=is_admin)
        return Response(status=status.HTTP_200_OK)

class AccountView(APIView, PaginationHandlerMixin):
    # permission_classes = (IsAdminUser, IsAuthenticated)
    pagination_class = Pagination

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties=SIGNUP_ACCOUNT_PROP))
    def put(self, request, pk):
        user = get_account(pk)
        update_account(user, request.data)
        return Response(status=status.HTTP_200_OK)

    def delete(self, request, pk):
        id = request.query_params.get('id')
        if id:
            delete_account(id)
            return Response("Delete successful")
        else:
            return Response({'id query param need to be provided'}, status=status.HTTP_400_BAD_REQUEST)


class PermissionView(APIView, PaginationHandlerMixin):
    permissions = (IsAdminUser, IsAuthenticated)
    pagination_class = Pagination

    def get(self, request):
        permissions = Permission.objects.all()

        id = request.query_params.get('id')
        sort = request.query_params.get('sort_by')
        if id:
            permissions = permissions.filter(id=id)
        if sort:
            permissions = permissions.order_by(f'{sort}')

        serializer = PermissionSerializer(permissions, many=True)
        page = self.paginate_queryset(permissions)
        if page is not None:
            serializer = self.get_paginated_response(PermissionSerializer(page, many=True).data)

        return Response(serializer.data)

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties=PERMISSION_PROP))
    def post(self, request):
        serializer = PermissionSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except serializers.ValidationError:
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        manual_parameters=[openapi.Parameter('id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='Permission id')],
    )
    def delete(self, request):
        id = request.query_params.get('id')
        if id:
            delete_permission(id)
            return Response("Delete successful")
        else:
            return Response({'id query param need to be provided'}, status=status.HTTP_400_BAD_REQUEST)
