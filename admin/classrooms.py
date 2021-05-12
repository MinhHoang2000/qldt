from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework import status, serializers
from rest_framework.response import Response
from config.pagination import Pagination, PaginationHandlerMixin

from school.models import Classroom
from school.serializers import ClassroomSerializer
from school.utils import get_classroom, delete_classroom


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
