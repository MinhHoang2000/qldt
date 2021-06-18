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


from config.settings import REST_FRAMEWORK

ORDERING_PARAM = REST_FRAMEWORK['ORDERING_PARAM']

class AchievementView(APIView, PaginationHandlerMixin):
    # permission_classes = (IsAdminUser, IsAuthenticated)
    pagination_class = Pagination

    def get(self, request):
        achievements = Achievement.objects.all()

        # queryset
        id = request.query_params.get('id')
        sort = request.query_params.get(ORDERING_PARAM)
        if id:
            achievements = achievements.filter(id=id)
        if sort:
            achievements = achievements.order_by(f'{sort}')


        serializer = AchievementSerializer(achievements, many=True)
        page = self.paginate_queryset(achievements)
        if page:
            serializer = self.get_paginated_response(AchievementSerializer(page, many=True).data)
        return Response(serializer.data)

    def post(self, request):
        achievement = AchievementSerializer(data=request.data)
        try:
            achievement.is_valid(raise_exception=True)
            achievement.save()
            return Response(achievement.data, status=status.HTTP_201_CREATED)
        except serializers.ValidationError:
            return Response(achievement.errors, status=status.HTTP_400_BAD_REQUEST)

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

    def get(self, request):
        id = request.query_params.get('student_id')

        sort = request.query_params.get(ORDERING_PARAM)

        if id:
            student = get_student(id)
            serializer = StudentAchievementSerializer(student)
        else:
            students = Student.objects.filter(achievements__isnull=False).distinct()
            if sort:
                students = students.order_by(f'{sort}')
            serializer = StudentAchievementSerializer(students, many=True)
            page = self.paginate_queryset(students)
            if page:
                serializer = self.get_paginated_response(StudentAchievementSerializer(page, many=True).data)

        return Response(serializer.data)

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

    def get(self, request):
        id = request.query_params.get('teacher_id')
        sort = request.query_params.get(ORDERING_PARAM)
        if id:
            teacher = get_teacher(id)
            serializer = TeacherAchievementSerializer(teacher)
        else:
            teachers = Teacher.objects.filter(achievements__isnull=False).distinct()
            if sort:
                teachers = teachers.order_by(f'{sort}')
            serializer = TeacherAchievementSerializer(teachers, many=True)
            page = self.paginate_queryset(teachers)
            if page:
                serializer = self.get_paginated_response(TeacherAchievementSerializer(page, many=True).data)

        return Response(serializer.data)

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
