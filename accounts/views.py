from rest_framework import status, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .serializers import *
from django.contrib.auth import authenticate, get_user_model
from rest_framework.authtoken.models import Token


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


class ProfileView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        if request.user.is_admin:
            response = 'This account is admin'
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        elif request.user.student.exists():
            student = request.user.student.first()
            profile = StudentProfileSerializer(student)
        else:
            teacher = request.user.teacher.first()
            profile = TeacherProfileSerializer(teacher)

        return Response(profile.data)
