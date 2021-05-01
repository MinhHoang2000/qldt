from .models import Student, Parent
from rest_framework import exceptions


def get_student(pk):
    try:
        student = Student.objects.get(pk=pk)
        return student
    except Student.DoesNotExist:
        raise exceptions.NotFound('Student does not exist')


def get_parent(pk):
    try:
        parent = Parent.objects.get(pk=pk)
        return student
    except Parent.DoesNotExist:
        raise exceptions.NotFound('Parent does not exist')
