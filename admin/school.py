from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.parsers import FileUploadParser, JSONParser, MultiPartParser
from rest_framework import status, serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework.response import Response
from config.pagination import Pagination, PaginationHandlerMixin

from school.models import Course, Device, StudyDocument, TeachingInfo, DeviceManage
from school.serializers import CourseSerializer, DeviceSerializer, DeviceManageSerializer, StudyDocumentSerializer, TeachingInfoSerializer
from school.utils import get_course, delete_course, get_device, delete_device, get_device_manage, get_file, delete_file, get_teaching_info, delete_teaching_info

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from school.schema import COURSE_PROP, COURSE_REQUIRED, DEVICE_PROP, DEVICE_REQUIRED, DEVICE_MANAGE_PROP, DEVICE_MANAGE_REQUIRED, STUDY_DOC_PROP, STUDY_DOC_REQUIRED

from config import settings
import os
import mimetypes
from django.http import HttpResponse

from config.settings import REST_FRAMEWORK

ORDERING_PARAM = REST_FRAMEWORK['ORDERING_PARAM']

# Course
class CourseView(APIView, PaginationHandlerMixin):
    # permission_classes = (IsAdminUser, IsAuthenticated)
    pagination_class = Pagination

    @swagger_auto_schema(
        manual_parameters=[openapi.Parameter('sort', openapi.IN_QUERY, type=openapi.TYPE_STRING, description='course_name or group_course')],
    )
    def get(self, request):
        courses = Course.objects.all()

        # Get query params for sort
        sort = request.query_params.get(ORDERING_PARAM)

        if sort:
            courses = courses.order_by(f'{sort}')

        serializer = CourseSerializer(courses, many=True)
        page = self.paginate_queryset(courses)
        if page:
            serializer = self.get_paginated_response(CourseSerializer(page, many=True).data)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties=COURSE_PROP,
        required=COURSE_REQUIRED))
    def post(self, request):
        serializer = CourseSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except serializers.ValidationError:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        manual_parameters=[openapi.Parameter('id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='Course id')],
        request_body=openapi.Schema(type=openapi.TYPE_OBJECT,
                                    properties=COURSE_PROP)
    )
    def put(self, request):
        id = request.query_params.get('id')
        if id:
            course = get_course(id)
            serializer = CourseSerializer(course, data=request.data, partial=True)
            try:
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data)
            except serializers.ValidationError:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'id query param need to be provided'}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        manual_parameters=[openapi.Parameter('id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='Course id')],
    )
    def delete(self, request):
        id = request.query_params.get('id')
        if id:
            delete_couse(id)
            return Response('Delete successful')
        else:
            return Response({'id query param need to be provided'}, status=status.HTTP_400_BAD_REQUEST)


# Device
class DeviceView(APIView, PaginationHandlerMixin):
    # permission_classes = (IsAdminUser, IsAuthenticated)
    pagination_class = Pagination

    @swagger_auto_schema(
        manual_parameters=[openapi.Parameter('sort', openapi.IN_QUERY, type=openapi.TYPE_STRING, description='status, device_name, amount or price')],
    )
    def get(self, request):
        devices = Device.objects.all()

        # Get query param for sort
        sort = request.query_params.get(ORDERING_PARAM)

        if sort:
            devices = devices.order_by(f'{sort}')

        serializer = DeviceSerializer(devices, many=True)
        page = self.paginate_queryset(devices)
        if page:
            serializer = self.get_paginated_response(DeviceSerializer(page, many=True).data)

        return Response(serializer.data)


class DeviceAddView(APIView):
    # permission_classes = (IsAdminUser, IsAuthenticated)

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties=DEVICE_PROP,
        required=DEVICE_REQUIRED))
    def post(self, request):
        serializer = DeviceSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except serializers.ValidationError:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeviceChangeDeleteView(APIView):
    # permission_classes = (IsAdminUser, IsAuthenticated)

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties=DEVICE_PROP))
    def put(self, request, pk):
        device = get_device(pk)
        serializer = DeviceSerializer(device, data=request.data, partial=True)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        except serializers.ValidationError:
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        delete_device(pk)
        return Response({'Delete successful'})


class DeviceManageView(APIView, PaginationHandlerMixin):
    # permission_classes = (IsAdminUser, IsAuthenticated)
    pagination_class = Pagination

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('device_id', openapi.IN_QUERY, description="Device id", type=openapi.TYPE_INTEGER),
            openapi.Parameter('teacher_id', openapi.IN_QUERY, description="Teacher id", type=openapi.TYPE_INTEGER),
            openapi.Parameter('sort', openapi.IN_QUERY, type=openapi.TYPE_STRING, description='day_of_week, shifts, week'),
            openapi.Parameter('week', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='Week'),
            openapi.Parameter('shifts', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='Shifts'),
            openapi.Parameter('day_of_week', openapi.IN_QUERY, type=openapi.TYPE_STRING, description='Day of week'),
        ],

    )
    def get(self, request):
        device_id = request.query_params.get('device_id')
        teacher_id = request.query_params.get('teacher_id')
        week = request.query_params.get('week')
        shifts = request.query_params.get('shifts')
        day_of_week = request.query_params.get('day_of_week')
        sort = request.query_params.get(ORDERING_PARAM)

        device_manages = DeviceManage.objects.all()

        # query params
        if(device_id):
            device_manages = device_manages.filter(device_id=device_id)
        if teacher_id:
            device_manages = device_manages.filter(teacher_id=teacher_id)
        if week:
            device_manages = device_manages.filter(week=week)
        if shifts:
            device_manages = device_manages.filter(shifts=shifts)
        if day_of_week:
            device_manages = device_manages.filter(day_of_week=day_of_week)
        if sort:
            device_manages = device_manages.order_by(f'{sort}')

        serializer = DeviceManageSerializer(device_manages, many=True)

        page = self.paginate_queryset(device_manages)
        if page:
            serializer = self.get_paginated_response(DeviceManageSerializer(page, many=True).data)

        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties=DEVICE_MANAGE_PROP,
            required=DEVICE_MANAGE_REQUIRED)
    )
    def post(self, request):
        serializer = DeviceManageSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except serializers.ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        manual_parameters=[openapi.Parameter('id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='Device manage id')],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties=DEVICE_MANAGE_PROP)
    )
    def put(self, request):
        device_manage_id = request.query_params.get('id')
        if device_manage_id:
            device_manage = get_device_manage(device_manage_id)
            serializer = DeviceManageSerializer(device_manage, data=request.data, partial=True)
            try:
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data)
            except serializers.ValidationError as error:
                return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'id query param need to be provided'}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        manual_parameters=[openapi.Parameter('id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='Device manage id')],
    )
    def delete(self, request):
        device_manage_id = request.query_params.get('id')
        if device_manage_id:
            delete_device_manage(device_manage_id)
            return Response({'Delete successful'})
        else:
            return Response({'device_manage_id query param need to be provided'}, status=status.HTTP_400_BAD_REQUEST)


# StudyDocument
class StudyDocumentView(APIView, PaginationHandlerMixin):
    # permission_classes = (IsAdminUser, IsAuthenticated)
    pagination_class = Pagination
    parser_classes = (JSONParser, MultiPartParser, FileUploadParser)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('teacher_id', openapi.IN_QUERY, description="Teacher id", type=openapi.TYPE_INTEGER),
            openapi.Parameter('course_id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='Course id'),
            openapi.Parameter('classroom_id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='Classroom id'),
            openapi.Parameter('sort', openapi.IN_QUERY, type=openapi.TYPE_STRING, description='name'),
            openapi.Parameter('study_week', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='Study week'),
        ],

    )
    def get(self, request):
        files = StudyDocument.objects.all()

        # Get query params
        sort = request.query_params.get(ORDERING_PARAM)
        course_id = request.query_params.get('course_id')
        teacher_id = request.query_params.get('teacher_id')
        classroom_id = request.query_params.get('classroom_id')
        study_week = request.query_params.get('study_week')

        if course_id:
            files = files.filter(course_id=course_id)
        if teacher_id:
            files = files.filter(teacher_id=teacher_id)
        if classroom_id:
            files = files.filter(classroom_id=classroom_id)
        if study_week:
            files = files.filter(study_week=study_week)
        if sort:
            files = files.order_by(f'{sort}')


        serializer = StudyDocumentSerializer(files, many=True)

        page = self.paginate_queryset(files)
        if page:
            serializer = self.get_paginated_response(StudyDocumentSerializer(page, many=True).data)

        return Response(serializer.data)


    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties=STUDY_DOC_PROP,
            required=STUDY_DOC_REQUIRED,
        )
    )
    def post(self, request):
        serializer = StudyDocumentSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response('Upload file successful')
        except serializers.ValidationError:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @swagger_auto_schema(
        manual_parameters=[openapi.Parameter('id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='File id')],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties=STUDY_DOC_PROP
        )
    )
    def put(self, request):
        id = request.query_params.get('id')
        if id:
            file = get_file(id)
            serializer = StudyDocumentSerializer(file, data=request.data, partial=True)
            try:
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data)

            except serializers.ValidationError:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'id query param need to be provided'}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        manual_parameters=[openapi.Parameter('id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='File id')],
    )
    def delete(self, request):
        id = request.query_params.get('id')
        if id:
            file = delete_file(id)
            return Response({'Delete successful'})
        else:
            return Response({'id query param need to be provided'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', ])
# @permission_classes([IsAuthenticated, IsAdminUser, ])
def download(request, pk):
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
