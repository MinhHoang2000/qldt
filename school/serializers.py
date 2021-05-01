from rest_framework import serializers
from .models import Classroom, Course
from teachers.serializers import TeacherSerializer


class ClassroomSerializer(serializers.ModelSerializer):
    homeroom_teacher_id = serializers.IntegerField()
    student_id = serializers.PrimaryKeyRelatedField(source='students', many=True, read_only=True)

    class Meta:
        model = Classroom
        fields = ['id', 'class_name', 'homeroom_teacher_id', 'location', 'student_id']

    def create(self, validated_data):
        return Classroom.objects.create(**validated_data)

class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = '__all__'
