from .models import Classroom


def get_classroom(pk):
    return Classroom.objects.get(pk=pk)


def assign_classroom_by_id(student, class_pk):
    classroom = Classroom.objects.get(pk=class_pk)
    student.classroom = classroom


