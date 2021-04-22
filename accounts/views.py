from rest_framework import status, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .serializers import *
from django.contrib.auth import authenticate, get_user_model


class LoginView(APIView):

    def post(self, request):
        credential = JSONParser().parse(request)

        try:
            account = authenticate(**credential)
            if account == None:
                return Response('Your password is wrong', status=status.HTTP_401_UNAUTHORIZED)
            else:
                data = AuthAccountSerializer(account).data
                return Response(data, status=status.HTTP_200_OK)
        except get_user_model().DoesNotExist:
            return Response('Account does not exist', status=status.HTTP_401_UNAUTHORIZED)


class RegisterView(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)

    def post(self, request):
        account = AccountRegisterSerializer(data=request.data)

        try:
            account.is_valid(raise_exception=True)
        except serializers.ValidationError:
            return Response(account.errors, status=status.HTTP_400_BAD_REQUEST)
        account.save()
        return Response(status=status.HTTP_200_OK)


class ChangePasswordView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        account = ChangePasswordSerializer(data=request.data, context={'request': request})

        try:
            account.is_valid(raise_exception=True)
            request.user.set_password(account.validated_data['new_password'])
            request.user.save()
        except serializers.ValidationError:
            return Response(account.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_200_OK)

