from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework import status, serializers
from rest_framework.response import Response
from config.pagination import Pagination, PaginationHandlerMixin

from school.models import Classroom
from school.serializers import ClassroomSerializer, TimetableSerializer, RecordSerializer
from school.utils import get_classroom, get_timetable, get_record

# Classroom


class ClassroomView(APIView, PaginationHandlerMixin):
    # permission_classes = (IsAdminUser, IsAuthenticated)
    pagination_class = Pagination

    def get(self, request):
        classrooms = Classroom.objects.all()
        id = request.query_params.get('id')
        if id:
            classrooms = classrooms.filter(id=id)

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
class ClassTimetableView(APIView, PaginationHandlerMixin):
    # permission_classes = (IsAdminUser, IsAuthenticated)
    pagination_class = Pagination

    def get(self, request):
        class_id = request.query_params.get('class_id')
        if class_id:
            classroom = get_classroom(class_id)
            timetables = classroom.timetables.all()

            time_id = request.query_params.get('time_id')
            if time_id:
                timetables = timetables.filter(id=time_id)

            serializer = TimetableSerializer(timetables, many=True)

            page = self.paginate_queryset(timetables)
            if page:
                serializer = self.get_paginated_response(TimetableSerializer(page, many=True).data)
            return Response(serializer.data)

        else:
            return Response({'class_id query param need to be provided'}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        class_id = request.query_params.get('class_id')
        if class_id:
            request.data.update({'classroom_id': class_id})
            timetable = TimetableSerializer(data=request.data)
            try:
                timetable.is_valid(raise_exception=True)
                timetable.save()
                return Response(timetable.data, status=status.HTTP_201_CREATED)
            except serializers.ValidationError:
                return Response(timetable.errors, status=status.HTTP_400_BAD_REQUEST)

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

            except serializers.ValidationError:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({'time_id query param need to be provided'}, status=status.HTTP_400_BAD_REQUEST)


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
            record_id = request.query_params.get('record_id')
            if study_week:
                records = records.filter(study_week=study_week)

            if record_id:
                records = records.filter(id=record_id)

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
            except serializers.ValidationError:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
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

            except serializers.ValidationError:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'record_id query param need to be provided'}, status=status.HTTP_400_BAD_REQUEST)
