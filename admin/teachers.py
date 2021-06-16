from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework import status, serializers
from rest_framework.response import Response
from config.pagination import Pagination, PaginationHandlerMixin

from teachers.models import Teacher
from teachers.serializers import TeacherSerializer
from teachers.utils import get_teacher, delete_teacher


class TeacherView(APIView, PaginationHandlerMixin):
    # permission_classes = (IsAdminUser, IsAuthenticated)
    pagination_class = Pagination

    def get(self, request):
        teachers = Teacher.objects.all()

        # Get query param for id or sort
        id = request.query_params.get('id')
        sort = request.query_params.get('sort_by')

        if id:
            teachers = teachers.filter(id=id)
        if sort:
            teachers = teachers.order_by(f'{sort}')


        serializer = TeacherSerializer(teachers, many=True)
        page = self.paginate_queryset(teachers)
        if page:
            serializer = self.get_paginated_response(TeacherSerializer(page, many=True).data)

        return Response(serializer.data)

    def post(self, request):
        teacher = TeacherSerializer(data=request.data)
        try:
            teacher.is_valid(raise_exception=True)
            teacher.save()
            return Response(data=teacher.data, status=status.HTTP_201_CREATED)
        except serializers.ValidationError:
            return Response(teacher.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        id = request.query_params.get('id')
        if id:
            teacher = get_teacher(id)
            serializer = TeacherSerializer(teacher, data=request.data, partial=True)
            try:
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

            except serializers.ValidationError:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'id query param need to be provide'})

    def delete(self, request):
        id = request.query_params.get('id')
        if id:
            delete_teacher(id)
            return Response({'Delete successful'})
        else:
            return Response({'id query param need to be provide'})
