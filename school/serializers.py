from rest_framework import serializers

from .models import Classroom, Course, Timetable, ClassRecord, Device, DeviceManage, StudyDocument, TeachingInfo
from teachers.models import Teacher

from teachers.serializers import TeacherSerializer


from .validations import validate_classroom_timetable, validate_teacher_timetable, validate_classroom_record, validate_classroom_attendant, validate_device_manage
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
    classroom = ClassroomSerializer()
    teacher = TeacherSerializer()
    course = CourseSerializer()

    class Meta:
        model = Timetable
        fields = ['id', 'day_of_week', 'shifts', 'semester', 'school_year', 'course', 'teacher', 'classroom']

    def create(self, validated_data):
        classroom_id = validated_data.get('classroom_id')
        teacher_id = validated_data.get('teacher_id')
        day_of_week = validated_data.get('day_of_week')
        shifts = validated_data.get('shifts')
        semester = validated_data.get('semester')
        school_year = validated_data.get('school_year')

        validate_classroom_timetable(classroom_id, day_of_week, shifts, semester, school_year)
        validate_teacher_timetable(teacher_id, day_of_week, shifts, semester, school_year)

        return Timetable.objects.create(**validated_data)

    def update(self, instance, validated_data):
        try:
            teacher_id = validated_data.pop('teacher_id')
            validate_teacher_timetable(teacher_id, instance.day_of_week, instance.shifts)
            instance.teacher_id = teacher_id
        except KeyError:
            pass

        instance.course_id = validated_data.get('course_id', instance.course_id)
        instance.save()
        return instance


class RecordSerializer(serializers.ModelSerializer):
    classroom = ClassroomSerializer()
    teacher = TeacherSerializer()
    course = CourseSerializer()
    total_student = serializers.SerializerMethodField()

    class Meta:
        model = ClassRecord
        fields = ['id', 'classroom_id', 'teacher_id', 'course_id', 'day_of_week', 'shifts', 'study_week', 'total_student', 'attendant', 'note', 'semester', 'school_year']

    def create(self, validated_data):
        classroom_id = validated_data.get('classroom_id')
        day_of_week = validated_data.get('day_of_week')
        shifts = validated_data.get('shifts')
        study_week = validated_data.get('study_week')
        semester = validated_data.get('semester')
        school_year = validated_data.get('school_year')
        attendant = validated_data.get('attendant')

        validate_classroom_record(classroom_id, day_of_week, shifts, study_week, semester, school_year)
        validate_classroom_attendant(classroom_id, attendant)

        return ClassRecord.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.teacher_id = validated_data.get('teacher_id', instance.teacher_id)
        instance.course_id = validated_data.get('course_id', instance.course_id)

        try:
            attendant = validated_data.pop('attendant')
            validate_classroom_attendant(instance.classroom_id, attendant)
        except KeyError:
            pass

        instance.attendant = validated_data.get('attendant', instance.attendant)
        instance.note = validated_data.get('note', instance.note)
        instance.save()
        return instance

    def get_total_student(self, obj):
        total = obj.classroom.students.count()
        return total


class DeviceManageSerializer(serializers.ModelSerializer):
    device_id = serializers.IntegerField(write_only=True)
    teacher_id = serializers.IntegerField()

    class Meta:
        model = DeviceManage
        fields = ['id', 'day_of_week', 'week', 'shifts', 'teacher_id', 'device_id']

    def create(self, validated_data):
        device_id = validated_data.get('device_id')
        week = validated_data.get('week')
        day_of_week = validated_data.get('day_of_week')
        shifts = validated_data.get('shifts')
        validate_device_manage(device_id, week, day_of_week, shifts)
        return DeviceManage.objects.create(**validated_data)

    def update(self, instance, validated_data):
        teacher_id = validated_data.get('teacher_id', instance.account_id)
        week = validated_data.get('week', instance.week)
        day_of_week = validated_data.get('day_of_week', instance.day_of_week)
        shifts = validated_data.get('shifts', instance.shifts)

        validate_device_manage(instance.device_id, week, day_of_week, shifts)

        instance.teacher_id = teacher_id
        instance.week = week
        instance.day_of_week = day_of_week
        instance.shifts = shifts

        instance.save()
        return instance


class DeviceSerializer(serializers.ModelSerializer):
    device_manages = DeviceManageSerializer(many=True, read_only=True)

    class Meta:
        model = Device
        fields = ['id', 'status', 'device_name', 'device_manages', 'amount', 'price']


class StudyDocumentSerializer(serializers.ModelSerializer):
    teacher_id = serializers.IntegerField()
    course_id = serializers.IntegerField()
    classroom_id = serializers.IntegerField()

    class Meta:
        model = StudyDocument
        fields = ['id', 'name', 'file', 'study_week', 'teacher_id', 'course_id', 'classroom_id']
        extra_kwargs = {'file': {'write_only': True}}


class TeachingInfoSerializer(serializers.ModelSerializer):
    teacher_id = serializers.IntegerField()
    course_id = serializers.IntegerField()
    classroom_id = serializers.IntegerField()
    class Meta:
        model = TeachingInfo
        fields = ['id', 'school_year', 'semester', 'classroom_id', 'teacher_id', 'course_id']
