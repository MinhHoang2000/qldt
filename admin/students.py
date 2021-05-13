from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework import status, serializers
from rest_framework.response import Response
from config.pagination import Pagination, PaginationHandlerMixin

from students.models import Student, Parent, Grade
from students.serializers import StudentSerializer, ParentSerializer, GradeSerializer
from students.utils import get_student, get_parent, get_grade, delete_student, delete_grade, delete_parent


# Student
class StudentView(APIView, PaginationHandlerMixin):
    permission_classes = (IsAdminUser, IsAuthenticated)
    pagination_class = Pagination

    def get(self, request):
        students = Student.objects.all()

        # query_set
        id = request.query_params.get('id')
        status = request.query_params.get('status')
        admission_year = request.query_params.get('admission_year')
        if id:
            students = students.filter(id=id)
        if status:
            students = students.filter(status=status)
        if admission_year:
            students = students.filter(admission_year=admission_year)

        serializer = StudentSerializer(students, many=True)

        # paginate
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
            return Response({'id query param need to be provided'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        id = request.query_params.get('id')
        if id:
            delete_student(id)
            return Response({'Delete successful'})
        else:
            return Response({'id query param need to be provided'}, status=status.HTTP_400_BAD_REQUEST)


class StudentGradeView(APIView, PaginationHandlerMixin):
    permission_classes = (IsAdminUser, IsAuthenticated)
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

            serializer = GradeSerializer(grades, many=True)

            # paginate
            page = self.paginate_queryset(grades)
            if page:
                serializer = self.get_paginated_response(GradeSerializer(page, many=True).data)
            return Response(serializer.data)
        else:
            return Response({'student id query param need to be provided'}, status=status.HTTP_400_BAD_REQUEST)

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
            return Response({'student id query param need to be provided'}, status=status.HTTP_400_BAD_REQUEST)

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
            return Response('grade_id query param need to be provided', status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        # Need id
        grade_id = request.query_params.get('grade_id')
        if grade_id:
            delete_grade(id)
            return Response({'Delete successful'})
        else:
            return Response('grade_id query param need to be provided', status=status.HTTP_400_BAD_REQUEST)


# Parent
class ParentView(APIView, PaginationHandlerMixin):
    permission_classes = (IsAdminUser, IsAuthenticated)
    pagination_class = Pagination

    def get(self, request):
        parents = Parent.objects.all()
        id = request.query_params.get('id')
        if id:
            parents = parents.filter(id=id)

        serializer = ParentSerializer(parents, many=True)
        page = self.paginate_queryset(parents)
        if page:
            serializer = self.get_paginated_response(ParentSerializer(page, many=True).data)

        return Response(serializer.data)

    def post(self, request):
        parent = ParentSerializer(data=request.data)
        try:
            parent.is_valid(raise_exception=True)
            parent.save()
            return Response(data=parent.data, status=status.HTTP_201_CREATED)
        except serializers.ValidationError:
            return Response(parent.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        id = request.query_params.get('id')
        if id:
            parent = get_parent(id)
            serializer = ParentSerializer(parent, data=request.data, partial=True)
            try:
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            except serializers.ValidationError:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response('id query param need to be provided', status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        id = request.query_params.get('id')
        if id:
            delete_parent(id)
            return Response({'Delete successful'})
        else:
            return Response('id query param need to be provided', status=status.HTTP_400_BAD_REQUEST)
