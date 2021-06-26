from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework import status, serializers
from rest_framework.response import Response
from config.pagination import Pagination, PaginationHandlerMixin

from students.models import Student, Parent, Grade, Conduct
from students.serializers import StudentSerializer, ParentSerializer, GradeSerializer, ConductSerializer
from students.utils import get_student, get_parent, get_grade, get_conduct, delete_student, delete_grade, delete_parent


from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from students.schema import STUDENT_PROP, STUDENT_REQUIRED, GRADE_PROP, GRADE_REQUIRED, CONDUCT_PROP, CONDUCT_REQUIRED, PARENT_PROP, PARENT_REQUIRED
from config.settings import REST_FRAMEWORK

ORDERING_PARAM = REST_FRAMEWORK['ORDERING_PARAM']


# Student
class StudentView(APIView, PaginationHandlerMixin):
    # permission_classes = (IsAdminUser, IsAuthenticated)
    pagination_class = Pagination

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('classroom_id', openapi.IN_QUERY, description="Classroom id", type=openapi.TYPE_INTEGER),
            openapi.Parameter('status', openapi.IN_QUERY, description="Status", type=openapi.TYPE_STRING),
            openapi.Parameter('admission_year', openapi.IN_QUERY, description="Admission year", type=openapi.TYPE_INTEGER),
            openapi.Parameter('sort', openapi.IN_QUERY, type=openapi.TYPE_STRING, description='admission_year, status, person__first_name, person__last_name'),
        ],

    )
    def get(self, request):
        students = Student.objects.all()

        # query_set
        status = request.query_params.get('status')
        admission_year = request.query_params.get('admission_year')
        classroom_id = request.query_params.get('classroom_id')
        sort = request.query_params.get(ORDERING_PARAM)

        if status:
            students = students.filter(status=status)
        if admission_year:
            students = students.filter(admission_year=admission_year)
        if classroom_id:
            students = students.filter(classroom_id=classroom_id)
        if sort:
            students = students.order_by(f'{sort}')

        serializer = StudentSerializer(students, many=True)

        # paginate
        page = self.paginate_queryset(students)
        if page:
            serializer = self.get_paginated_response(StudentSerializer(page, many=True).data)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties=STUDENT_PROP,
        required=STUDENT_REQUIRED
    ))
    def post(self, request):
        student = StudentSerializer(data=request.data)
        try:
            student.is_valid(raise_exception=True)
            student.save()
            return Response(data=student.data, status=status.HTTP_201_CREATED)
        except serializers.ValidationError:
            return Response(student.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description='Partial update',
        manual_parameters=[openapi.Parameter('id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='Student id')],
        request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties=STUDENT_PROP
    ))
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

    @swagger_auto_schema(
        manual_parameters=[openapi.Parameter('id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='Student id')],
    )
    def delete(self, request):
        id = request.query_params.get('id')
        if id:
            delete_student(id)
            return Response({'Delete successful'})
        else:
            return Response({'id query param need to be provided'}, status=status.HTTP_400_BAD_REQUEST)


class StudentGradeView(APIView, PaginationHandlerMixin):
    # permission_classes = (IsAdminUser, IsAuthenticated)
    pagination_class = Pagination

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('student_id', openapi.IN_QUERY, description="Student id", type=openapi.TYPE_INTEGER),
            openapi.Parameter('classroom_id', openapi.IN_QUERY, description="Classroom id", type=openapi.TYPE_INTEGER),
            openapi.Parameter('course_id', openapi.IN_QUERY, description="Course id", type=openapi.TYPE_INTEGER),
            openapi.Parameter('school_year', openapi.IN_QUERY, description="School year", type=openapi.TYPE_STRING),
            openapi.Parameter('semester', openapi.IN_QUERY, description="Semester", type=openapi.TYPE_INTEGER),
            openapi.Parameter('sort', openapi.IN_QUERY, type=openapi.TYPE_STRING, description='final_test, mid_term_test'),
        ],
    )
    def get(self, request):
        grades = Grade.objects.all()

        # query_set
        student_id = request.query_params.get('student_id')
        classroom_id = request.query_params.get('classroom_id')
        course_id = request.query_params.get('course_id')
        semester = request.query_params.get('semester')
        school_year = request.query_params.get('school_year')
        sort = request.query_params.get(ORDERING_PARAM)

        if student_id:
            grades = grades.filter(student_id=student_id)
        if classroom_id:
            grades = grades.filter(student__classroom__id=classroom_id)
        if course_id:
            grades = grades.filter(course_id=course_id)
        if semester:
            grades = grades.filter(semester=semester)
        if school_year:
            grades = grades.filter(school_year=school_year)
        if sort:
            grades = grades.order_by(f'{sort}')

        serializer = GradeSerializer(grades, many=True)

        # paginate
        page = self.paginate_queryset(grades)
        if page:
            serializer = self.get_paginated_response(GradeSerializer(page, many=True).data)
        return Response(serializer.data)


    @swagger_auto_schema(
        request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties=GRADE_PROP,
        required=GRADE_REQUIRED,
        ),
    )
    def post(self, request):
        serializer = GradeSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except serializers.ValidationError:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        manual_parameters=[openapi.Parameter('id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='Grade id')],
        request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties=GRADE_PROP,
        ),
    )
    def put(self, request):
        # Need id
        grade_id = request.query_params.get('id')
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
            return Response('id query param need to be provided', status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        manual_parameters=[openapi.Parameter('id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='Grade id')],
    )
    def delete(self, request):
        # Need id
        grade_id = request.query_params.get('id')
        if grade_id:
            delete_grade(id)
            return Response({'Delete successful'})
        else:
            return Response('id query param need to be provided', status=status.HTTP_400_BAD_REQUEST)

class StudentConductView(APIView, PaginationHandlerMixin):
    # permission_classes = (IsAdminUser, IsAuthenticated)
    pagination_class = Pagination

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('school_year', openapi.IN_QUERY, description="School year", type=openapi.TYPE_STRING),
            openapi.Parameter('semester', openapi.IN_QUERY, description="Semester", type=openapi.TYPE_INTEGER),
            openapi.Parameter('sort', openapi.IN_QUERY, type=openapi.TYPE_STRING, description='score'),
        ],

    )
    def get(self, request):
        conducts = Conduct.objects.all()

        # query_set
        semester = request.query_params.get('semester')
        school_year = request.query_params.get('school_year')
        sort = request.query_params.get(ORDERING_PARAM)

        if semester:
            conducts = conducts.filter(term=semester)
        if school_year:
            conducts = conducts.filter(school_year=school_year)
        if sort:
            conducts = conducts.order_by(f'{sort}')

        serializer = ConductSerializer(conducts, many=True)

        # paginate
        page = self.paginate_queryset(conducts)
        if page:
            serializer = self.get_paginated_response(ConductSerializer(page, many=True).data)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties=CONDUCT_PROP,
        required=CONDUCT_REQUIRED,
        ),
    )
    def post(self, request):
        serializer = ConductSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except serializers.ValidationError:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @swagger_auto_schema(
        manual_parameters=[openapi.Parameter('id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='Conduct id')],
        request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties=CONDUCT_PROP,
        ),
    )
    def put(self, request):
        # Need id
        id = request.query_params.get('id')
        if id:
            conduct = get_conduct(id)
            serializer = ConductSerializer(conduct, data=request.data, partial=True)
            try:
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data)
            except serializers.ValidationError:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response('id query param need to be provided', status=status.HTTP_400_BAD_REQUEST)


    @swagger_auto_schema(
        manual_parameters=[openapi.Parameter('id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='Grade id')],
    )
    def delete(self, request):
        id = request.query_params.get('id')
        if id:
            delete_conduct(id)
            return Response({'Delete successful'})
        else:
            return Response('id query param need to be provided', status=status.HTTP_400_BAD_REQUEST)


# Parent
class ParentView(APIView, PaginationHandlerMixin):
    # permission_classes = (IsAdminUser, IsAuthenticated)
    pagination_class = Pagination

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('sort', openapi.IN_QUERY, type=openapi.TYPE_STRING, description='person__first_name, person__last_name'),
        ],

    )
    def get(self, request):
        parents = Parent.objects.all()
        sort = request.query_params.get(ORDERING_PARAM)

        if sort:
            parents = parents.order_by(f'{sort}')

        serializer = ParentSerializer(parents, many=True)
        page = self.paginate_queryset(parents)
        if page:
            serializer = self.get_paginated_response(ParentSerializer(page, many=True).data)

        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties=PARENT_PROP,
        required=PARENT_REQUIRED,
        ),
    )
    def post(self, request):
        parent = ParentSerializer(data=request.data)
        try:
            parent.is_valid(raise_exception=True)
            parent.save()
            return Response(data=parent.data, status=status.HTTP_201_CREATED)
        except serializers.ValidationError:
            return Response(parent.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        manual_parameters=[openapi.Parameter('id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='Parent id')],
        request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties=PARENT_PROP,
        ),
    )
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


    @swagger_auto_schema(
        manual_parameters=[openapi.Parameter('id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='Grade id')],
    )
    def delete(self, request):
        id = request.query_params.get('id')
        if id:
            delete_parent(id)
            return Response({'Delete successful'})
        else:
            return Response('id query param need to be provided', status=status.HTTP_400_BAD_REQUEST)
