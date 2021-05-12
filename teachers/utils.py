from rest_framework import exceptions
from .serializers import TeacherSerializer
from .models import Teacher


def get_teacher(pk):
    try:
        teacher = Teacher.objects.get(pk=pk)
        return teacher
    except Teacher.DoesNotExist:
        raise exceptions.NotFound('Teacher does not exist')


def create_teacher(teacher_data):
    teacher = TeacherSerializer(data=teacher_data)
    teacher.is_valid(raise_exception=True)
    return teacher.save()


def update_teacher(teacher, teacher_data):
    teacher_serializer = TeacherSerializer(teacher, data=teacher_data)
    teacher_serializer.is_valid(raise_exception=True)
    teacher_serializer.save()


def delete_teacher(pk):
    return get_teacher(pk).delete()
