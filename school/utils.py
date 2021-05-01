from rest_framework import exceptions
from .models import Classroom, Course


def get_classroom(pk):
    try:
        classroom = Classroom.objects.get(pk=pk)
        return classroom
    except Classroom.DoesNotExist:
        raise exceptions.NotFound('Classroom does not exist')


def assign_classroom_by_id(student, class_pk):
    classroom = Classroom.objects.get(pk=class_pk)
    student.classroom = classroom


def get_course(pk):
    try:
        return Course.objects.get(pk=pk)
    except Course.DoesNotExist:
        raise exceptions.NotFound('Course does not exist')
