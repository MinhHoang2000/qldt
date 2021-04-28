from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from accounts.permissions import IsOwner
from rest_framework import status, serializers, exceptions
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import *

from students.models import Student
from teachers.models import Teacher
from students.serializers import StudentSerializer
from teachers.serializers import TeacherSerializer
from accounts.serializers import AccountSerializer
from accounts.utils import create_account, update_account


class RegisterView(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)

    def post(self, request):
        try:
            create_account(request.data, is_admin=True)
        except serializers.ValidationError:
            return Response(account.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK)


class UpdateView(APIView):
    permission_classes = (IsAdminUser, IsAuthenticated, IsOwner)

    def post(self, request):
        try:
            update_account(request.user, request.data)
        except serializers.ValidationError:
            return Response(account.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_200_OK)


class StudentListView(APIView):
    permission_classes = (IsAdminUser, IsAuthenticated)

    def get(self, request):
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)

    def post(self, request):
        student = StudentSerializer(data=request.data)
        try:
            student.is_valid(raise_exception=True)
            student.save()
            return Response(data=student.data, status=status.HTTP_201_CREATED)
        except serializers.ValidationError:
            return Response(student.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentDetailView(APIView):
    permission_classes = (IsAdminUser, IsAuthenticated)

    def get_student(self, pk):
        try:
            student = Student.objects.get(pk=pk)
            return student
        except Teacher.DoesNotExist:
            raise exceptions.NotFound('Student does not exist')

    def get(self, request, pk):
        student = self.get_student(pk)
        serializer = StudentSerializer(student)
        return Response(serializer.data)

    def put(self, request, pk):
        student = self.get_student(pk)
        serializer = StudentSerializer(student, data=request.data, partial=True)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except serializers.ValidationError:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TeacherListView(APIView):
    permission_classes = (IsAdminUser, IsAuthenticated)

    def get(self, request):
        teachers = Teacher.objects.all()
        serializer = TeacherSerializer(teachers, many=True)
        return Response(serializer.data)

    def post(self, request):
        teacher = TeacherSerializer(data=request.data)
        try:
            teacher.is_valid(raise_exception=True)
            teacher.save()
            return Response(data=teacher.data, status=status.HTTP_201_CREATED)
        except serializers.ValidationError:
            return Response(teacher.errors, status=status.HTTP_400_BAD_REQUEST)


class TeacherDetailView(APIView):
    permission_classes = (IsAdminUser, IsAuthenticated)

    def get_teacher(self, pk):
        try:
            teacher = Teacher.objects.get(pk=pk)
            return teacher
        except Teacher.DoesNotExist:
            raise exceptions.NotFound('Teacher does not exist')

    def get(self, request, pk):
        teacher = self.get_teacher(pk)
        serializer = TeacherSerializer(teacher)
        return Response(serializer.data)

    def put(self, request, pk):
        teacher = self.get_teacher(pk)
        serializer = TeacherSerializer(teacher, data=request.data, partial=True)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        except serializers.ValidationError:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
