from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from accounts.permissions import IsOwner

from rest_framework import status, serializers
from rest_framework.response import Response

from django.contrib.auth import get_user_model

from .serializers import *
from config.pagination import Pagination, PaginationHandlerMixin

from accounts.models import Permission
from teachers.models import Teacher
from school.models import Classroom, Course
from django.contrib.auth import get_user_model

from teachers.serializers import TeacherSerializer
from accounts.serializers import AccountSerializer, PermissionSerializer
from school.serializers import ClassroomSerializer, CourseSerializer, TimetableSerializer, RecordSerializer

from accounts.utils import create_account, update_account, delete_account
from teachers.utils import get_teacher
from school.utils import get_classroom, get_course, get_timetable, get_record


from .students import *
from .achievements import *

import logging
logger = logging.getLogger(__name__)


# Account
class RegisterView(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)

    def post(self, request):
        account = create_account(request.data, is_admin=True)
        return Response(status=status.HTTP_200_OK)


class UpdateView(APIView):
    permission_classes = (IsAdminUser, IsAuthenticated)

    def put(self, request):
        update_account(request.user, request.data)
        return Response(status=status.HTTP_200_OK)


class AccountView(APIView, PaginationHandlerMixin):
    permission_classes = (IsAdminUser, IsAuthenticated)
    pagination_class = Pagination

    def get(self, request):
        accounts = get_user_model().objects.all()

        username = request.query_params.get('username')
        id = request.query_params.get('id')
        if username:
            accounts = accounts.filter(username=username)
        if id:
            accounts = accounts.filter(id=id)

        serializer = AccountSerializer(accounts, many=True)
        page = self.paginate_queryset(accounts)
        if page is not None:
            serializer = self.get_paginated_response(AccountSerializer(page, many=True).data)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request):
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

        serializer = PermissionSerializer(permissions, many=True)
        page = self.paginate_queryset(permissions)
        if page is not None:
            serializer = self.get_paginated_response(PermissionSerializer(page, many=True).data)

        return Response(serializer.data)

    def post(self, request):
        serializer = PermissionSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except serializers.ValidationError:
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


# Teacher
class TeacherListView(APIView):
    # permission_classes = (IsAdminUser, IsAuthenticated)

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

    def get(self, request, pk):
        teacher = get_teacher(pk)
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


# Classroom
class ClassroomListView(APIView):
    # permission_classes = (IsAdminUser, IsAuthenticated)

    def get(self, request):
        classrooms = Classroom.objects.all()
        serializer = ClassroomSerializer(classrooms, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        classroom = ClassroomSerializer(data=request.data)
        try:
            classroom.is_valid(raise_exception=True)
            classroom.save()
            return Response(classroom.data, status=status.HTTP_201_CREATED)

        except serializers.ValidationError:
            return Response(classroom.errors, status=status.HTTP_400_BAD_REQUEST)


class ClassroomDetailView(APIView):
    permission_classes = (IsAdminUser, IsAuthenticated)

    def get(self, request, pk):
        classroom = get_classroom(pk)
        serializer = ClassroomSerializer(classroom)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        classroom = get_classroom(pk)
        serializer = ClassroomSerializer(classroom, data=request.data, partial=True)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except serializers.ValidationError:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Course
class CourseView(APIView, PaginationHandlerMixin):
    # permission_classes = (IsAdminUser, IsAuthenticated)
    pagination_class = Pagination

    def get(self, request):
        courses = Course.objects.all()

        id = request.query_params.get('id')
        if id is not None:
            courses = courses.filter(id=id)
        serializer = CourseSerializer(courses, many=True)

        page = self.paginate_queryset(courses)
        if page is not None:
            serializer = self.get_paginated_response(CourseSerializer(page, many=True).data)
        return Response(serializer.data)

    def post(self, request):
        course = CourseSerializer(data=request.data)
        try:
            course.is_valid(raise_exception=True)
            course.save()
            return Response(course.data, status=status.HTTP_201_CREATED)
        except serializers.ValidationError:
            return Response(course.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        id = request.query_params.get('id')
        if id is not None:
            course = get_course(id)
            serializer = CourseSerializer(course, data=request.data, partial=True)
            try:
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data)
            except serializers.ValidationError:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'id query param need to be provided'}, status=status.HTTP_400_BAD_REQUEST)


# Timetable
class ClassTimetableView(APIView):
    permission_classes = (IsAdminUser, IsAuthenticated)

    def get(self, request, pk):
        classroom = get_classroom(pk)
        timetables = classroom.timetables.all()
        serializer = TimetableSerializer(timetables, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        request.data.update({'classroom_id': pk})
        timetable = TimetableSerializer(data=request.data)
        try:
            timetable.is_valid(raise_exception=True)
            timetable.save()
            return Response(timetable.data, status=status.HTTP_201_CREATED)
        except serializers.ValidationError:
            return Response(timetable.errors, status=status.HTTP_400_BAD_REQUEST)


class ClassTimetableDetailView(APIView):
    permission_classes = (IsAdminUser, IsAuthenticated)

    def get(self, request, class_pk, timetable_pk):
        timetable = get_timetable(timetable_pk)
        serializer = TimetableSerializer(timetable)
        return Response(serializer.data)

    def put(self, request, class_pk, timetable_pk):
        request.data.update({'classroom_id': class_pk})
        timetable = get_timetable(timetable_pk)
        serializer = TimetableSerializer(timetable, data=request.data, partial=True)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

        except serializers.ValidationError:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Record
class ClassRecordView(APIView):
    permission_classes = (IsAdminUser, IsAuthenticated)

    def get(self, request, pk):
        classroom = get_classroom(pk)
        records = classroom.classrecords.all()
        serializer = RecordSerializer(records, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        request.data.update({'classroom_id': pk})
        serializer = RecordSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except serializers.ValidationError:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClassRecordDetailView(APIView):
    permission_classes = (IsAdminUser, IsAuthenticated)

    def get(self, request, class_pk, record_pk):
        record = get_record(record_pk)
        serializer = RecordSerializer(record)
        return Response(serializer.data)

    def put(self, request, class_pk, record_pk):
        record = get_record(record_pk)
        serializer = RecordSerializer(record, data=request.data, partial=True)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

        except serializers.ValidationError:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
