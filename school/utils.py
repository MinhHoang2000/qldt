from rest_framework import exceptions
from .models import Classroom, Course, Timetable, ClassRecord


def get_classroom(pk):
    try:
        classroom = Classroom.objects.get(pk=pk)
        return classroom
    except Classroom.DoesNotExist:
        raise exceptions.NotFound('Classroom does not exist')


def delete_classroom(pk):
    return get_classroom(pk).delete()


def assign_classroom_by_id(student, class_pk):
    classroom = Classroom.objects.get(pk=class_pk)
    student.classroom = classroom


def get_course(pk):
    try:
        return Course.objects.get(pk=pk)
    except Course.DoesNotExist:
        raise exceptions.NotFound('Course does not exist')


def delete_course(pk):
    return get_course(pk).delete()


def get_timetable(pk):
    try:
        timetable = Timetable.objects.get(pk=pk)
        return timetable
    except Timetable.DoesNotExist:
        raise exceptions.NotFound('Timetable does not exist')


def delete_timetable(pk):
    return get_timetable(pk).delete()


def get_record(pk):
    try:
        record = ClassRecord.objects.get(pk=pk)
        return record
    except ClassRecord.DoesNotExist:
        raise exceptions.NotFound('Class record does not exist')


def delete_record(pk):
    return get_record(pk).delete()
