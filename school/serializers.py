from rest_framework import serializers

from .models import Classroom, Course, Timetable
from teachers.models import Teacher

from teachers.serializers import TeacherSerializer

from .validations import validate_classroom_timetable, validate_teacher_timetable
import logging
logger = logging.getLogger(__name__)


class ClassroomSerializer(serializers.ModelSerializer):
    homeroom_teacher_id = serializers.IntegerField()
    student_id = serializers.PrimaryKeyRelatedField(source='students', many=True, read_only=True)

    class Meta:
        model = Classroom
        fields = ['id', 'class_name', 'homeroom_teacher_id', 'location', 'student_id']


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = '__all__'


class TimetableSerializer(serializers.ModelSerializer):
    classroom_id = serializers.IntegerField()
    teacher_id = serializers.IntegerField()
    course_id = serializers.IntegerField()

    class Meta:
        model = Timetable
        fields = ['id', 'classroom_id', 'teacher_id', 'course_id', 'day_of_week', 'shifts']

    def validate(self, data):
        logger.error(data)
        validate_classroom_timetable(data['classroom_id'], data['day_of_week'], data['shifts'])
        validate_teacher_timetable(data['teacher_id'], data['day_of_week'], data['shifts'])
        return data
