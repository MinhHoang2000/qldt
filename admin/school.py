from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.parsers import FileUploadParser, JSONParser, MultiPartParser
from rest_framework import status, serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework.response import Response
from config.pagination import Pagination, PaginationHandlerMixin

from school.models import Course, Device, StudyDocument, TeachingInfo
from school.serializers import CourseSerializer, DeviceSerializer, DeviceManageSerializer, StudyDocumentSerializer, TeachingInfoSerializer
from school.utils import get_course, delete_course, get_device, delete_device, get_device_manage, get_file, delete_file, get_teaching_info, delete_teaching_info

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from school.schema import COURSE_PROP, COURSE_REQUIRED, DEVICE_PROP, DEVICE_REQUIRED

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

    def get(self, request):
        courses = Course.objects.all()

        # Get query params for sort or id
        id = request.query_params.get('id')
        sort = request.query_params.get(ORDERING_PARAM)

        if id:
            courses = courses.filter(id=id)
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

    def get(self, request):
        devices = Device.objects.all()

        # Get query param for id or sort
        id = request.query_params.get('id')
        sort = request.query_params.get(ORDERING_PARAM)
        if id:
            devices = devices.filter(id=id)
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
        delete_device(id)
        return Response({'Delete successful'})


class DeviceManageView(APIView, PaginationHandlerMixin):
    # permission_classes = (IsAdminUser, IsAuthenticated)
    pagination_class = Pagination

    def get(self, request):
        device_id = request.query_params.get('device_id')
        if device_id:
            device = get_device(device_id)
            device_manages = device.device_manages.all()

            # Get query param for sort
            sort = request.query_params.get(ORDERING_PARAM)
            if sort:
                device_manages = device_manages.order_by(f'{sort}')

            serializer = DeviceManageSerializer(device_manages, many=True)

            page = self.paginate_queryset(device_manages)
            if page:
                serializer = self.get_paginated_response(DeviceManageSerializer(page, many=True).data)

            return Response(serializer.data)

        else:
            return Response({'device_id query param need to be provided'}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        device_id = request.query_params.get('device_id')
        if device_id:
            request.data.update({'device_id': device_id})
            serializer = DeviceManageSerializer(data=request.data)
            try:
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except serializers.ValidationError as error:
                return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'device_id query param need to be provided'}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        device_manage_id = request.query_params.get('device_manage_id')
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
            return Response({'device_manage_id query param need to be provided'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        device_manage_id = request.query_params.get('device_manage_id')
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

    def get(self, request):
        files = StudyDocument.objects.all()

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

    def post(self, request):
        serializer = StudyDocumentSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response('Upload file successful')
        except serializers.ValidationError:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
