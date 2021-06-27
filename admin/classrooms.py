from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework import status, serializers
from rest_framework.response import Response
from config.pagination import Pagination, PaginationHandlerMixin

from school.models import Classroom, Timetable, ClassRecord
from school.serializers import ClassroomSerializer, TimetableSerializer, RecordSerializer
from school.utils import get_classroom, get_timetable, get_record, delete_timetable, delete_record
from students.utils import get_student

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from school.schema import CLASSROOM_PROP, CLASSROOM_REQUIRED, TIMETABLE_REQURIED, TIMETABLE_PROP, TIMETABLE_CHANGE_PROP,CLASSRECORD_PROP, CLASSRECORD_REQUIRED, CLASSRECORD_CHANGE_PROP

from config.settings import REST_FRAMEWORK

ORDERING_PARAM = REST_FRAMEWORK['ORDERING_PARAM']


# Classroom
class ClassroomView(APIView, PaginationHandlerMixin):
    # permission_classes = (IsAdminUser, IsAuthenticated)
    pagination_class = Pagination

    @swagger_auto_schema(
        manual_parameters=[openapi.Parameter('sort', openapi.IN_QUERY, type=openapi.TYPE_STRING, description='class_name, location')],
    )
    def get(self, request):
        classrooms = Classroom.objects.all()

        # Query param
        sort = request.query_params.get(ORDERING_PARAM)
        if sort:
            classrooms = classrooms.order_by(f'{sort}')

        serializer = ClassroomSerializer(classrooms, many=True)

        page = self.paginate_queryset(classrooms)
        if page:
            serializer = self.get_paginated_response(ClassroomSerializer(page, many=True).data)

        return Response(serializer.data, status=status.HTTP_200_OK)


    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties=CLASSROOM_PROP,
        required=CLASSROOM_REQUIRED))
    def post(self, request):
        classroom = ClassroomSerializer(data=request.data)
        try:
            classroom.is_valid(raise_exception=True)
            classroom.save()
            return Response(classroom.data, status=status.HTTP_201_CREATED)

        except serializers.ValidationError:
            return Response(classroom.errors, status=status.HTTP_400_BAD_REQUEST)


    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_QUERY, description="Classroom id", type=openapi.TYPE_INTEGER)],
        request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties=CLASSROOM_PROP))
    def put(self, request):
        id = request.query_params.get('id')
        if id:
            classroom = get_classroom(id)
            serializer = ClassroomSerializer(classroom, data=request.data, partial=True)
            try:
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            except serializers.ValidationError:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'id query param need to be provided'}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_QUERY, description="Classroom id", type=openapi.TYPE_INTEGER)],
    )
    def delete(self, request):
        id = request.query_params.get('id')
        if id:
            delete_classroom(id)
            return Response({'Delete successful'})
        else:
            return Response({'id query param need to be provided'}, status=status.HTTP_400_BAD_REQUEST)


# Timetable
class TimetableView(APIView, PaginationHandlerMixin):
    # permission_classes = (IsAdminUser, IsAuthenticated)
    pagination_class = Pagination

    @swagger_auto_schema(
        manual_parameters=[openapi.Parameter('sort', openapi.IN_QUERY, type=openapi.TYPE_STRING, description='day_of_week, shifts, semester, school_year')],
    )
    def get(self, request):
        timetables = Timetable.objects.all()
        # Sort
        sort = request.query_params.get(ORDERING_PARAM)

        if sort:
            classrooms = timetables.order_by(f'{sort}')

        serializer = TimetableSerializer(timetables, many=True)

        page = self.paginate_queryset(timetables)
        if page:
            serializer = self.get_paginated_response(TimetableSerializer(page, many=True).data)
        return Response(serializer.data)


class TimetableCreateView(APIView):
    # permission_classes = (IsAdminUser, IsAuthenticated)

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties=TIMETABLE_PROP,
        required=TIMETABLE_REQURIED))
    def post(self, request):
        timetable = TimetableSerializer(data=request.data)
        try:
            timetable.is_valid(raise_exception=True)
            timetable.save()
            return Response(timetable.data, status=status.HTTP_201_CREATED)
        except serializers.ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)

class TimetableChangeView(APIView):
    # permission_classes = (IsAdminUser, IsAuthenticated)

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties=TIMETABLE_CHANGE_PROP))
    def put(self, request, pk):
        timetable = get_timetable(pk)
        serializer = TimetableSerializer(timetable, data=request.data, partial=True)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

        except serializers.ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)

class TimetableDeleteView(APIView):
    # permission_classes = (IsAdminUser, IsAuthenticated)
    def delete(self, request, pk):
        delete_timetable(pk)
        return Response({'Delete successful'})

class TimetableStudentView(APIView, PaginationHandlerMixin):
    # permission_classes = (IsAdminUser, IsAuthenticated)
    pagination_class = Pagination

    def get(self, request, pk):
        student = get_student(pk)
        timetable = Timetable.objects.filter(classroom=student.classroom)
        serializer = TimetableSerializer(timetable, many=True)

        page = self.paginate_queryset(timetable)
        if page:
            serializer = self.get_paginated_response(TimetableSerializer(page, many=True).data)
        return Response(serializer.data)


class SearchTimetableView(APIView, PaginationHandlerMixin):
    # permission_classes = (IsAdminUser, IsAuthenticated)
    pagination_class = Pagination

    def post(self, request):
        timetables = Timetable.objects.all()

        # Sort
        sort = request.query_params.get(ORDERING_PARAM)

        # Get search value
        teacher_name = request.data.get('teacher_name', '')
        class_name = request.data.get('class_name', '')
        course_name = request.data.get('course_name', '')

        timetables = timetables.filter(teacher__person__first_name__contains=teacher_name,
                          course__course_name__contains=course_name,
                          classroom__class_name__contains=class_name)

        serializer = TimetableSerializer(timetables, many=True)

        page = self.paginate_queryset(timetables)
        if page:
            serializer = self.get_paginated_response(TimetableSerializer(page, many=True).data)
        return Response(serializer.data)


# Record
class ClassRecordView(APIView, PaginationHandlerMixin):
    # permission_classes = (IsAdminUser, IsAuthenticated)
    pagination_class = Pagination

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('classroom_id', openapi.IN_QUERY, description="Classroom id", type=openapi.TYPE_INTEGER),
            openapi.Parameter('teacher_id', openapi.IN_QUERY, description="Teacher id", type=openapi.TYPE_INTEGER),
            openapi.Parameter('sort', openapi.IN_QUERY, type=openapi.TYPE_STRING, description='study_week, semester, school_year'),
            openapi.Parameter('study_week', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='Study Week'),
            openapi.Parameter('semester', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='Semester'),
            openapi.Parameter('school_year', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='School year'),

        ],

    )
    def get(self, request):

        records = ClassRecord.objects.all()
        # query_set
        class_id = request.query_params.get('classroom_id')
        teacher_id = request.query_params.get('teacher_id')
        study_week = request.query_params.get('study_week')
        semester = request.query_params.get('semester')
        school_year = request.query_params.get('school_year')

        sort = request.query_params.get(ORDERING_PARAM)

        if class_id :
            records = records.filter(classroom_id=class_id)
        if teacher_id :
            records = records.filter(teacher_id=teacer_id)
        if study_week:
            records = records.filter(study_week=study_week)
        if semester:
            records = records.filter(semester=semester)
        if school_year:
            records = records.filter(school_year=school_year)
        if sort:
            records = records.order_by(f'{sort}')

        serializer = RecordSerializer(records, many=True)

        # paginate
        page = self.paginate_queryset(records)
        if page:
            serializer = self.get_paginated_response(RecordSerializer(page, many=True).data)

        return Response(serializer.data)


    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties=CLASSRECORD_PROP,
        required=CLASSRECORD_REQUIRED))
    def post(self, request):
        serializer = RecordSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except serializers.ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        manual_parameters=[ openapi.Parameter('id', openapi.IN_QUERY, description="Class record id", type=openapi.TYPE_INTEGER)],
        request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties=CLASSRECORD_CHANGE_PROP))
    def put(self, request):
        record_id = request.query_params.get('id')
        if record_id:
            record = get_record(record_id)
            serializer = RecordSerializer(record, data=request.data, partial=True)
            try:
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data)

            except serializers.ValidationError as error:
                return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'id query param need to be provided'}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        manual_parameters=[ openapi.Parameter('id', openapi.IN_QUERY, description="Class record id", type=openapi.TYPE_INTEGER)],)
    def delete(self, request):
        record_id = request.query_params.get('id')
        if record_id:
            delete_record(record_id)
            return Response({'Delete successful'})
        else:
            return Response({'id query param need to be provided'}, status=status.HTTP_400_BAD_REQUEST)
