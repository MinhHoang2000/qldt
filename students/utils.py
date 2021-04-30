from .models import Student


def get_student(pk):
    try:
        student = Student.objects.get(pk=pk)
        return student
    except Student.DoesNotExist:
        raise exceptions.NotFound('Student does not exist')
