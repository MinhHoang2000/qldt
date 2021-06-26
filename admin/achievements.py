from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from rest_framework import status, serializers
from rest_framework.response import Response
from config.pagination import Pagination, PaginationHandlerMixin

from persons.models import Achievement
from students.models import Student
from teachers.models import Teacher

from .serializers import StudentAchievementSerializer, TeacherAchievementSerializer
from persons.serializers import AchievementSerializer

from persons.utils import get_achievement, delete_achievement
from students.utils import get_student
from teachers.utils import get_teacher

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from persons.schema import ACHIEVEMENT_PROP, ACHIEVEMENT_REQUIRED, ACHIEVEMENT_STUDENT_PROP, ACHIEVEMENT_TEACHER_PROP

from config.settings import REST_FRAMEWORK

ORDERING_PARAM = REST_FRAMEWORK['ORDERING_PARAM']

class AchievementView(APIView, PaginationHandlerMixin):
    # permission_classes = (IsAdminUser, IsAuthenticated)
    pagination_class = Pagination

    @swagger_auto_schema(
        manual_parameters=[openapi.Parameter('sort', openapi.IN_QUERY, type=openapi.TYPE_STRING, description='achievement_name, created_at')],
    )
    def get(self, request):
        achievements = Achievement.objects.all()

        # queryset
        sort = request.query_params.get(ORDERING_PARAM)

        if sort:
            achievements = achievements.order_by(f'{sort}')


        serializer = AchievementSerializer(achievements, many=True)
        page = self.paginate_queryset(achievements)
        if page:
            serializer = self.get_paginated_response(AchievementSerializer(page, many=True).data)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties=ACHIEVEMENT_PROP,
        required=ACHIEVEMENT_REQUIRED))
    def post(self, request):
        achievement = AchievementSerializer(data=request.data)
        try:
            achievement.is_valid(raise_exception=True)
            achievement.save()
            return Response(achievement.data, status=status.HTTP_201_CREATED)
        except serializers.ValidationError:
            return Response(achievement.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        manual_parameters=[openapi.Parameter('id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='Achievement id')],
        request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties=ACHIEVEMENT_PROP))
    def put(self, request):
        id = request.query_params.get('id')
        if id:
            achievement = get_achievement(id)
            serializer = AchievementSerializer(achievement, data=request.data, partial=True)
            try:
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data)
            except serializers.ValidationError:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({'id query param need to be provided'}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        manual_parameters=[openapi.Parameter('id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='Achievement id')],
    )
    def delete(self, request):
        id = request.query_params.get('id')
        if id:
            delete_achievement(id)
            return Response("Delete successful")
        else:
            return Response({'id query param need to be provided'}, status=status.HTTP_400_BAD_REQUEST)


class StudentAchievementView(APIView, PaginationHandlerMixin):
    # permission_classes = (IsAdminUser, IsAuthenticated)
    pagination_class = Pagination

    @swagger_auto_schema(
        manual_parameters=[openapi.Parameter('sort', openapi.IN_QUERY, type=openapi.TYPE_STRING, description='achievement_name, created_at'),
                           openapi.Parameter('classroom_id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='Classroom id')],
    )
    def get(self, request):
        sort = request.query_params.get(ORDERING_PARAM)
        classroom_id = request.query_params.get('classroom_id')
        students = Student.objects.filter(achievements__isnull=False).distinct()

        if classroom_id:
            students = students.filter(classroom_id=classroom_id)
        if sort:
            students = students.order_by(f'achievement__{sort}')
        serializer = StudentAchievementSerializer(students, many=True)
        page = self.paginate_queryset(students)
        if page:
            serializer = self.get_paginated_response(StudentAchievementSerializer(page, many=True).data)

        return Response(serializer.data)

    @swagger_auto_schema(
        manual_parameters=[
        openapi.Parameter('student_id', openapi.IN_QUERY, description="Student id", type=openapi.TYPE_INTEGER)],
        request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties=ACHIEVEMENT_STUDENT_PROP))
    def put(self, request):
        id = request.query_params.get('student_id')
        if id:
            student = get_student(id)
            serializer = StudentAchievementSerializer(student, data=request.data)
            try:
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

            except serializers.ValidationError:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'student_id query param need to be provided'}, status=status.HTTP_400_BAD_REQUEST)


class TeacherAchievementView(APIView, PaginationHandlerMixin):
    permission_classes = (IsAdminUser, IsAuthenticated)
    pagination_class = Pagination

    @swagger_auto_schema(
        manual_parameters=[openapi.Parameter('sort', openapi.IN_QUERY, type=openapi.TYPE_STRING, description='achievement_name, created_at')],
    )
    def get(self, request):
        sort = request.query_params.get(ORDERING_PARAM)
        teachers = Teacher.objects.filter(achievements__isnull=False).distinct()
        if sort:
            teachers = teachers.order_by(f'{sort}')
        serializer = TeacherAchievementSerializer(teachers, many=True)
        page = self.paginate_queryset(teachers)
        if page:
            serializer = self.get_paginated_response(TeacherAchievementSerializer(page, many=True).data)

        return Response(serializer.data)


    @swagger_auto_schema(
        manual_parameters=[
        openapi.Parameter('teacher_id', openapi.IN_QUERY, description="Teacher id", type=openapi.TYPE_INTEGER)],
        request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties=ACHIEVEMENT_TEACHER_PROP))
    def put(self, request):
        id = request.query_params.get('teacher_id')
        if id:
            teacher = get_teacher(id)
            serializer = TeacherAchievementSerializer(teacher, data=request.data)
            try:
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

            except serializers.ValidationError:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'teacher_id query param need to be provided'}, status=status.HTTP_400_BAD_REQUEST)
