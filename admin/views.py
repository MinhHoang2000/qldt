from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from accounts.permissions import IsOwner

from rest_framework import status, serializers
from rest_framework.response import Response
from django.contrib.auth import get_user_model

from .serializers import *

from accounts.models import Permission
from students.models import Student, Parent
from teachers.models import Teacher
from school.models import Classroom, Course
from persons.models import Achievement
from django.contrib.auth import get_user_model

from students.serializers import StudentSerializer, StudentGradeSerializer, ParentSerializer, GradeSerializer
from teachers.serializers import TeacherSerializer
from accounts.serializers import AccountSerializer, PermissionSerializer
from school.serializers import ClassroomSerializer, CourseSerializer, TimetableSerializer, RecordSerializer
from persons.serializers import AchievementSerializer

from accounts.utils import create_account, update_account
from students.utils import get_student, get_parent, get_grade
from teachers.utils import get_teacher
from school.utils import get_classroom, get_course, get_timetable, get_record
from persons.utils import get_achievement

import logging
logger = logging.getLogger(__name__)


# Account
class RegisterView(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)

    def post(self, request):
        try:
            create_account(request.data, is_admin=True)
        except serializers.ValidationError:
            return Response(account.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK)


class UpdateView(APIView):
    permission_classes = (IsAdminUser, IsAuthenticated)

    def post(self, request):
        try:
            update_account(request.user, request.data)
        except serializers.ValidationError:
            return Response(account.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_200_OK)


class AccountListView(APIView):
    permission_classes = (IsAdminUser, IsAuthenticated)

    def get(self, request):
        accounts = get_user_model().objects.all()

        username = request.query_params.get('username')
        id = request.query_params.get('id')
        if username is not None:
            accounts = accounts.filter(username=username)
        if id is not None:
            accounts = accounts.filter(id=int(id))

        serializer = AccountSerializer(accounts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PermissionView(APIView):
    permissions = (IsAdminUser, IsAuthenticated)

    def get(self, request):
        permissions = Permission.objects.all()
        serializer = PermissionSerializer(permissions, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PermissionSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except serializers.ValidationError:
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


# Student
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

    def get(self, request, pk):
        student = get_student(pk)
        serializer = StudentSerializer(student)
        return Response(serializer.data)

    def put(self, request, pk):
        student = get_student(pk)
        serializer = StudentSerializer(student, data=request.data, partial=True)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except serializers.ValidationError:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentAchievementListView(APIView):
    permission_classes = (IsAdminUser, IsAuthenticated)

    def get(self, request):
        students = Student.objects.filter(achievements__isnull=False).distinct()
        serializer = StudentAchievementSerializer(students, many=True)
        return Response(serializer.data)


class StudentAchievementDetailView(APIView):
    permission_classes = (IsAdminUser, IsAuthenticated)

    def get(self, request, pk):
        student = get_student(pk)
        serializer = StudentAchievementSerializer(student)
        return Response(serializer.data)

    def put(self, request, pk):
        student = get_student(pk)
        serializer = StudentAchievementSerializer(student, data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        except serializers.ValidationError:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentGradeListView(APIView):
    permission_classes = (IsAdminUser, IsAuthenticated)

    def get(self, request, pk):
        student = get_student(pk)
        serializer = StudentGradeSerializer(student)
        return Response(serializer.data)

    def post(self, request, pk):
        student = get_student(pk)
        serializer = StudentGradeSerializer(data=request.data, context={'student': student})
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except serializers.ValidationError:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentGradeDetailView(APIView):
    permission_classes = (IsAdminUser, IsAuthenticated)

    def get(self, request, student_pk, grade_pk):
        grade = get_grade(grade_pk)
        serializer = GradeSerializer(grade)
        return Response(serializer.data)

    def put(self, request, student_pk, grade_pk):
        grade = get_grade(grade_pk)
        serializer = GradeSerializer(grade, data=request.data, partial=True)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        except serializers.ValidationError:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Parent
class ParentListView(APIView):
    permission_classes = (IsAdminUser, IsAuthenticated)

    def get(self, request):
        parents = Parent.objects.all()
        serializer = ParentSerializer(parents, many=True)
        return Response(serializer.data)

    def post(self, request):
        parent = ParentSerializer(data=request.data)
        try:
            parent.is_valid(raise_exception=True)
            parent.save()
            return Response(data=parent.data, status=status.HTTP_201_CREATED)
        except serializers.ValidationError:
            return Response(parent.errors, status=status.HTTP_400_BAD_REQUEST)


class ParentDetailView(APIView):
    permission_classes = (IsAdminUser, IsAuthenticated)

    def get(self, request, pk):
        parent = get_parent(pk)
        serializer = ParentSerializer(student)
        return Response(serializer.data)

    def put(self, request, pk):
        parent = get_parent(pk)
        serializer = ParentSerializer(parent, data=request.data, partial=True)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except serializers.ValidationError:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Teacher
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


class TeacherAchievementListView(APIView):
    permission_classes = (IsAdminUser, IsAuthenticated)

    def get(self, request):
        teachers = Teacher.objects.filter(achievements__isnull=False).distinct()
        serializer = TeacherAchievementSerializer(teachers, many=True)
        return Response(serializer.data)


class TeacherAchievementDetailView(APIView):
    permission_classes = (IsAdminUser, IsAuthenticated)

    def get(self, request, pk):
        teacher = get_student(pk)
        serializer = TeacherAchievementSerializer(student)
        return Response(serializer.data)

    def put(self, request, pk):
        teacher = get_teacher(pk)
        serializer = TeacherAchievementSerializer(teacher, data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        except serializers.ValidationError:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Classroom
class ClassroomListView(APIView):
    permission_classes = (IsAdminUser, IsAuthenticated)

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
class CourseListView(APIView):
    permission_classes = (IsAdminUser, IsAuthenticated)

    def get(self, request):
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)

    def post(self, request):
        course = CourseSerializer(data=request.data)
        try:
            course.is_valid(raise_exception=True)
            course.save()
            return Response(course.data, status=status.HTTP_201_CREATED)
        except serializers.ValidationError:
            return Response(course.errors, status=status.HTTP_400_BAD_REQUEST)


class CourseDetailView(APIView):
    permission_classes = (IsAdminUser, IsAuthenticated)

    def get(self, request, pk):
        course = get_course(pk)
        serializer = CourseSerializer(course)
        return Response(serializer.data)

    def put(self, request, pk):
        course = get_course(pk)
        serializer = CourseSerializer(course, data=request.data, partial=True)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

        except serializers.ValidationError:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


# Achievement
class AchievementListView(APIView):
    permission_classes = (IsAdminUser, IsAuthenticated)

    def get(self, request):
        achievements = Achievement.objects.all()
        serializer = AchievementSerializer(achievements, many=True)
        return Response(serializer.data)

    def post(self, request):
        achievement = AchievementSerializer(data=request.data)
        try:
            achievement.is_valid(raise_exception=True)
            achievement.save()
            return Response(achievement.data, status=status.HTTP_201_CREATED)
        except serializers.ValidationError:
            return Response(achievement.errors, status=status.HTTP_400_BAD_REQUEST)


class AchievementDetailView(APIView):
    permission_classes = (IsAdminUser, IsAuthenticated)

    def get(self, request, pk):
        achievement = get_achievement(pk)
        serializer = AchievementSerializer(achievement)
        return Response(serializer.data)

    def put(self, request, pk):
        achievement = get_achievement(pk)
        serializer = AchievementSerializer(achievement, data=request.data, partial=True)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        except serializers.ValidationError:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
