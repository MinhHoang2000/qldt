from rest_framework.views import APIView

from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.parsers import FileUploadParser, JSONParser, MultiPartParser
from rest_framework.decorators import api_view, permission_classes
from accounts.permissions import IsOwner
from config.pagination import Pagination, PaginationHandlerMixin
from rest_framework import status, serializers
from rest_framework.response import Response
from django.contrib.auth import get_user_model

from .serializers import *

from students.models import Student, Parent
from teachers.models import Teacher
from school.models import Classroom, Course, Timetable, StudyDocument
from persons.models import Achievement
from django.contrib.auth import get_user_model

from students.serializers import StudentSerializer, ParentSerializer, GradeSerializer
from school.serializers import ClassroomSerializer, CourseSerializer, TimetableSerializer, StudyDocumentSerializer
from persons.serializers import AchievementSerializer
from students.utils import get_student, get_parent, get_grade, get_conduct
from teachers.utils import get_teacher
from school.utils import get_file
from persons.utils import get_achievement

import os
from config import settings
import mimetypes
from django.http import HttpResponse
from config.settings import REST_FRAMEWORK

ORDERING_PARAM = REST_FRAMEWORK['ORDERING_PARAM']

#Account
class StudentInfoView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        try:
            student = Student.objects.get(account=user)
        except Exception:
            raise serializers.ValidationError('Your account is don\'t have permissions to acess this information')

        serializer = StudentSerializer(student)
        return Response(serializer.data)

class ClassroomInfoView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        try:
            student = Student.objects.get(account=user)
        except Exception:
            raise serializers.ValidationError('Your account is don\'t have permissions to acess this information')

        classroom = get_classroom(pk=student.classroom.id)
        serializer = ClassroomSerializer(classroom)
        return Response(serializer.data)


class ParentListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        try:
            student = Student.objects.get(account=user)
        except Exception:
            raise serializers.ValidationError('Your account is don\'t have permissions to acess this information')

        parents = student.parents.all()
        serializer = ParentSerializer(parents, many=True)
        return Response(serializer.data)

class AchievementListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        try:
            student = Student.objects.get(account=user)
        except Exception:
            raise serializers.ValidationError('Your account is don\'t have permissions to acess this information')

        achivement = student.achievements.all()
        serializer = AchievementSerializer(achivement, many=True)
        return Response(serializer.data)


#TimeTable
class TimeTableView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        try:
            student = Student.objects.get(account=user)
        except Exception:
            raise serializers.ValidationError('Your account is don\'t have permissions to acess this information')
        timetables = Timetable.objects.filter(classroom=student.classroom)
        school_year = request.query_params.get('school_year')
        semester = request.query_params.get('semester')
        if school_year:
            timetables = timetables.filter(school_year=school_year)

        if semester:
            timetables = timetables.filter(semester=semester)

        serializer = TimetableSerializer(timetable, many=True)
        return Response(serializer.data)


#Grade
class GradeListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        try:
            student = Student.objects.get(account=user)
        except Exception:
            raise serializers.ValidationError('Your account is don\'t have permissions to acess this information')
        grades = student.grades.all()

        school_year = request.query_params.get('school_year')
        semester = request.query_params.get('semester')

        if school_year:
            grades = grades.filter(school_year=school_year)

        if semester:
            grades = grades.filter(semester=semester)


        serializer = GradeSerializer(grades, many=True)
        return Response(serializer.data)

#Conduct
class ConductListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        try:
            student = Student.objects.get(account=user)
        except Exception:
            raise serializers.ValidationError('Your account is don\'t have permissions to acess this information')
        conducts = student.conduct.all()

        school_year = request.query_params.get('school_year')
        semester = request.query_params.get('semester')

        if school_year:
            conducts = conducts.filter(school_year=school_year)

        if semester:
            conducts = conducts.filter(semester=semester)

        serializer = ConductSerializer(conducts, many=True)
        return Response(serializer.data)

class StudyDocumentView(APIView, PaginationHandlerMixin):
    permission_classes = [IsAuthenticated,]
    pagination_class = Pagination
    parser_classes = (JSONParser, MultiPartParser, FileUploadParser)

    def get(self, request):
        user = request.user
        try:
            student = Student.objects.get(account=user)
        except Exception:
            raise serializers.ValidationError('Your account is don\'t have permissions to acess this information')

        files = StudyDocument.objects.filter(classroom=student.classroom)

        # Get query param for id or sort
        id = request.query_params.get('id')
        sort = request.query_params.get(ORDERING_PARAM)
        course_id = request.query_params.get('course_id')
        teacher_id = request.query_params.get('teacher_id')

        if id:
            files = files.filter(id=id)
        if course_id:
            files = files.filter(course_id=course_id)
        if teacher_id:
            files = files.filter(teacher_id=teacher_id)
        if sort:
            files = files.order_by(f'{sort}')

        serializer = StudyDocumentSerializer(files, many=True)

        page = self.paginate_queryset(files)
        if page:
            serializer = self.get_paginated_response(StudyDocumentSerializer(page, many=True).data)

        return Response(serializer.data)

@api_view(['GET', ])
@permission_classes([IsAuthenticated,])
def download(request, pk):
    user = request.user
    try:
        student = Student.objects.get(account=user)
    except Exception:
        raise serializers.ValidationError('Your account is don\'t have permissions to acess this information')
    f = get_file(pk)
    filepath = os.path.join(settings.BASE_DIR, f.file.path)
    if os.path.exists(filepath):
        filename = os.path.basename(filepath)
        mimetype = mimetypes.guess_type(filepath)
        with open(filepath, 'rb') as f:
            response = HttpResponse(f.read(), content_type=mimetype)
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response
    else:
        return Response({'File not found'}, status=status.HTTP_404_NOT_FOUND)
