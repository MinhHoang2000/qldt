from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from rest_framework import status, serializers
from rest_framework.response import Response
from config.pagination import Pagination, PaginationHandlerMixin

from school.models import Course
from school.serializers import CourseSerializer
from school.utils import get_course


class CourseView(APIView, PaginationHandlerMixin):
    # permission_classes = (IsAdminUser, IsAuthenticated)
    pagination_class = Pagination

    def get(self, request):
        courses = Course.objects.all()

        id = request.query_params.get('id')
        if id is not None:
            courses = courses.filter(id=id)
        serializer = CourseSerializer(courses, many=True)

        page = self.paginate_queryset(courses)
        if page is not None:
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
        if id is not None:
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
