from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from accounts.permissions import IsOwner
from rest_framework import status, serializers
from rest_framework.response import Response
from config.pagination import Pagination, PaginationHandlerMixin

from students.models import Student, Parent, Grade
from students.serializers import StudentSerializer, ParentSerializer, GradeSerializer
from students.utils import get_student, get_parent, get_grade


class StudentView(APIView, PaginationHandlerMixin):
    # permission_classes = (IsAdminUser, IsAuthenticated)
    pagination_class = Pagination

    def get(self, request):
        students = Student.objects.all()

        # query_set
        id = request.query_params.get('id')
        status = request.query_params.get('status')
        admission_year = request.query_params.get('admission_year')
        if id:
            students = students.filter(id=int(id))
        if status:
            students = students.filter(status=status)
        if admission_year:
            students = students.filter(admission_year=admission_year)

        serializer = StudentSerializer(students, many=True)

        #paginate
        page = self.paginate_queryset(students)
        if page:
            serializer = self.get_paginated_response(StudentSerializer(page, many=True).data)
        return Response(serializer.data)

    def post(self, request):
        student = StudentSerializer(data=request.data)
        try:
            student.is_valid(raise_exception=True)
            student.save()
            return Response(data=student.data, status=status.HTTP_201_CREATED)
        except serializers.ValidationError:
            return Response(student.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        # Need id
        id = request.query_params.get('id')
        if id:
            student = get_student(id)
            serializer = StudentSerializer(student, data=request.data, partial=True)
            try:
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            except serializers.ValidationError:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            Response({'id query need to be provided'}, status=status.HTTP_400_BAD_REQUEST)


class StudentGradeView(APIView, PaginationHandlerMixin):
    # permission_classes = (IsAdminUser, IsAuthenticated)
    pagination_class = Pagination

    def get(self, request):
        student_id = request.query_params.get('student_id')
        if student_id:
            grades = Grade.objects.filter(student_id=student_id)

            # query_set
            term = request.query_params.get('term')
            school_year = request.query_params.get('school_year')
            if term:
                grades = grades.filter(term=term)
            if school_year:
                grades = grades.filter(school_year=school_year)

            serializer = GradeSerializer(grades)

            #paginate
            page = self.paginate_queryset(grades)
            if page:
                serializer = self.get_paginated_response(GradeSerializer(page, many=True).data)
            return Response(serializer.data)
        else:
            return Response({'student id param need to be provided'}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        student_id = request.query_params.get('student_id')
        if student_id:
            serializer = GradeSerializer(data=request.data, context={'student_id': student_id})
            try:
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except serializers.ValidationError:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'student id param need to be provided'}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        # Need id
        grade_id = request.query_params.get('grade_id')
        if grade_id:
            grade = get_grade(grade_id)
            serializer = GradeSerializer(grade, data=request.data, partial=True)
            try:
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data)
            except serializers.ValidationError:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response('grade_id query params need to be provided', status=status.HTTP_400_BAD_REQUEST)


class StudentAchievementListView(APIView):
    # permission_classes = (IsAdminUser, IsAuthenticated)

    def get(self, request):
        students = Student.objects.filter(achievements__isnull=False).distinct()
        serializer = StudentAchievementSerializer(students, many=True)
        return Response(serializer.data)


class StudentAchievementDetailView(APIView):
    # permission_classes = (IsAdminUser, IsAuthenticated)

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
