from rest_framework import status, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .serializers import *
from django.contrib.auth import authenticate, get_user_model
from rest_framework.authtoken.models import Token

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .schema import *
from persons.schema import PERSON_PROP

class LoginView(APIView):
    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties=ACCOUNT_PROP,
        required=ACCOUNT_REQUIRED))
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
    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties=CHANGE_PASS_PROP))
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
            return Response('This account is admin')
        elif request.user.student.exists():
            student = request.user.student.first()
            profile = StudentProfileSerializer(student)
        elif request.user.teacher.exists():
            teacher = request.user.teacher.first()
            profile = TeacherProfileSerializer(teacher)
        else:
            return Response('This account doesn\'t have any info')

        return Response(profile.data)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'person': openapi.Schema(type=openapi.TYPE_OBJECT, properties=PERSON_PROP, description='Personal Info'),
            }
        )
    )
    def put(self, request):
        user = request.user

        if user.student.exists():
            student = user.student.first()
            serializer = StudentProfileSerializer(student, request.data, partial=True)
        elif user.teacher.exists():
            teacher = user.teacher.first()
            serializer = TeacherProfileSerializer(teacher, request.data, partial=True)

        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except serializers.ValidationError:
            return Response(student.errors, status=status.HTTP_400_BAD_REQUEST)




