from rest_framework import serializers
from .models import Classroom
from teachers.serializers import TeacherSerializer


class ClassroomSerializer(serializers.ModelSerializer):
    homeroom_teacher = TeacherSerializer()

    class Meta:
        model = Classroom
        fields = ['id', 'class_name', 'homeroom_teacher', 'location']
