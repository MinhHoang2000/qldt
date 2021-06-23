from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework import status, serializers
from rest_framework.response import Response
from config.pagination import Pagination, PaginationHandlerMixin

from school.models import Classroom, Timetable
from school.serializers import ClassroomSerializer, TimetableSerializer, RecordSerializer
from school.utils import get_classroom, get_timetable, get_record, delete_timetable, delete_record

from config.settings import REST_FRAMEWORK

ORDERING_PARAM = REST_FRAMEWORK['ORDERING_PARAM']


# Classroom
class ClassroomView(APIView, PaginationHandlerMixin):
    # permission_classes = (IsAdminUser, IsAuthenticated)
    pagination_class = Pagination

    def get(self, request):
        classrooms = Classroom.objects.all()

        # Query param for id or sort
        id = request.query_params.get('id')
        sort = request.query_params.get(ORDERING_PARAM)
        if id:
            classrooms = classrooms.filter(id=id)
        if sort:
            classrooms = classrooms.order_by(f'{sort}')

        serializer = ClassroomSerializer(classrooms, many=True)

        page = self.paginate_queryset(classrooms)
        if page:
            serializer = self.get_paginated_response(ClassroomSerializer(page, many=True).data)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        classroom = ClassroomSerializer(data=request.data)
        try:
            classroom.is_valid(raise_exception=True)
            classroom.save()
            return Response(classroom.data, status=status.HTTP_201_CREATED)

        except serializers.ValidationError:
            return Response(classroom.errors, status=status.HTTP_400_BAD_REQUEST)

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

    def get(self, request):
        timetables = Timetable.objects.all()

        # Sort
        sort = request.query_params.get(ORDERING_PARAM)

        # Get by id
        time_id = request.query_params.get('time_id')
        if time_id:
            timetables = timetables.filter(id=time_id)

        if sort:
            classrooms = timetables.order_by(f'{sort}')

        serializer = TimetableSerializer(timetables, many=True)

        page = self.paginate_queryset(timetables)
        if page:
            serializer = self.get_paginated_response(TimetableSerializer(page, many=True).data)
        return Response(serializer.data)



    def post(self, request):
        class_id = request.query_params.get('class_id')
        if class_id:
            request.data.update({'classroom_id': class_id})
            timetable = TimetableSerializer(data=request.data)
            try:
                timetable.is_valid(raise_exception=True)
                timetable.save()
                return Response(timetable.data, status=status.HTTP_201_CREATED)
            except serializers.ValidationError as error:
                return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({'class_id query param need to be provided'}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        time_id = request.query_params.get('time_id')
        if time_id:
            timetable = get_timetable(time_id)
            serializer = TimetableSerializer(timetable, data=request.data, partial=True)
            try:
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data)

            except serializers.ValidationError as error:
                return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({'time_id query param need to be provided'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        time_id = request.query_params.get('time_id')
        if time_id:
            delete_timetable(time_id)
            return Response({'Delete successful'})
        else:
            return Response({'time_id query param need to be provided'}, status=status.HTTP_400_BAD_REQUEST)


class SearchTimetableView(APIView, PaginationHandlerMixin):
    # permission_classes = (IsAdminUser, IsAuthenticated)
    pagination_class = Pagination
    def get(self, request):
        timetables = Timetable.objects.all()

        # Sort
        sort = request.query_params.get(ORDERING_PARAM)

        # Get search value
        teacher_name = request.data.get('teacher_name', '')
        class_name = request.data.get('class_name', '')
        course_name = request.data.get('course_name', '')

        timetables.filter(teacher__person_first_name__contains=teacher_name,
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

    def get(self, request):
        class_id = request.query_params.get('class_id')
        if class_id:
            classroom = get_classroom(class_id)
            records = classroom.classrecords.all()
            # query_set
            study_week = request.query_params.get('study_week')
            semester = request.query_params.get('semester')
            school_year = request.query_params.get('school_year')

            record_id = request.query_params.get('record_id')
            sort = request.query_params.get(ORDERING_PARAM)

            if study_week:
                records = records.filter(study_week=study_week)

            if semester:
                records = records.filter(semester=semester)

            if school_year:
                records = records.filter(school_year=school_year)

            if record_id:
                records = records.filter(id=record_id)

            if sort:
                records = records.order_by(f'{sort}')

            serializer = RecordSerializer(records, many=True)

            # paginate
            page = self.paginate_queryset(records)
            if page:
                serializer = self.get_paginated_response(RecordSerializer(page, many=True).data)

            return Response(serializer.data)

        else:
            return Response({'class_id query param need to be provided'}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        class_id = request.query_params.get('class_id')
        if class_id:
            request.data.update({'classroom_id': class_id})
            serializer = RecordSerializer(data=request.data)
            try:
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except serializers.ValidationError as error:
                return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'class_id query param need to be provided'}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        record_id = request.query_params.get('record_id')
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
            return Response({'record_id query param need to be provided'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        record_id = request.query_params.get('record')
        if record_id:
            delete_record(record_id)
            return Response({'Delete successful'})
        else:
            return Response({'record_id query param need to be provided'}, status=status.HTTP_400_BAD_REQUEST)
