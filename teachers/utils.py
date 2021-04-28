from .serializers import TeacherSerializer


def create_teacher(teacher_data):
    teacher = TeacherSerializer(data=teacher_data)
    teacher.is_valid(raise_exception=True)
    return teacher.save()


def update_teacher(teacher, teacher_data):
    teacher_serializer = TeacherSerializer(teacher, data=teacher_data)
    teacher_serializer.is_valid(raise_exception=True)
    teacher_serializer.save()
