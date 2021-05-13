from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.parsers import FileUploadParser, JSONParser, MultiPartParser
from rest_framework import status, serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework.response import Response
from config.pagination import Pagination, PaginationHandlerMixin

from school.models import Course, Device, FileManage
from school.serializers import CourseSerializer, DeviceSerializer, DeviceManageSerializer, FileManageSerializer
from school.utils import get_course, delete_course, get_device, delete_device, get_device_manage, get_file, delete_file

from config import settings
import os
import mimetypes
from django.http import HttpResponse


# Course
class CourseView(APIView, PaginationHandlerMixin):
    permission_classes = (IsAdminUser, IsAuthenticated)
    pagination_class = Pagination

    def get(self, request):
        courses = Course.objects.all()

        id = request.query_params.get('id')
        if id:
            courses = courses.filter(id=id)
        serializer = CourseSerializer(courses, many=True)

        page = self.paginate_queryset(courses)
        if page:
            serializer = self.get_paginated_response(CourseSerializer(page, many=True).data)
        return Response(serializer.data)

    def post(self, request):
        course = CourseSerializer(data=request.data)
        try:
            course.is_valid(raise_exception=True)
            course.save()
            return Response(course.data, status=status.HTTP_201_CREATED)
        except serializers.ValidationError:
            return Response(course.errors, status=status.HTTP_400_BAD_REQUEST)

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
    permission_classes = (IsAdminUser, IsAuthenticated)
    pagination_class = Pagination

    def get(self, request):
        devices = Device.objects.all()
        id = request.query_params.get('id')
        if id:
            devices = devices.filter(id=id)

        serializer = DeviceSerializer(devices, many=True)
        page = self.paginate_queryset(devices)
        if page:
            serializer = self.get_paginated_response(DeviceSerializer(page, many=True).data)

        return Response(serializer.data)

    def post(self, request):
        serializer = DeviceSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except serializers.ValidationError:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        id = request.query_params.get('id')
        if id:
            device = get_device(id)
            serializer = DeviceSerializer(device, data=request.data, partial=True)
            try:
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data)
            except serializers.ValidationError:
                return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'id query param need to be provided'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        id = request.query_params.get('id')
        if id:
            delete_device(id)
            return Response({'Delete successful'})
        else:
            return Response({'id query param need to be provided'}, status=status.HTTP_400_BAD_REQUEST)


class DeviceManageView(APIView, PaginationHandlerMixin):
    permission_classes = (IsAdminUser, IsAuthenticated)
    pagination_class = Pagination

    def get(self, request):
        device_id = request.query_params.get('device_id')
        if device_id:
            device = get_device(device_id)
            device_manages = device.device_manages.all()

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


# File
class FileManageView(APIView, PaginationHandlerMixin):
    permission_classes = (IsAdminUser, IsAuthenticated)
    pagination_class = Pagination
    parser_classes = (JSONParser, MultiPartParser, FileUploadParser)

    def get(self, request):
        files = FileManage.objects.all()
        id = request.query_params.get('id')
        if id:
            files = files.filter(id=id)

        serializer = FileManageSerializer(files, many=True)

        page = self.paginate_queryset(files)
        if page:
            serializer = self.get_paginated_response(FileManageSerializer(page, many=True).data)

        return Response(serializer.data)

    def post(self, request):
        serializer = FileManageSerializer(data=request.data)
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
            serializer = FileManageSerializer(file, data=request.data, partial=True)
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
@permission_classes([IsAuthenticated, IsAdminUser, ])
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
