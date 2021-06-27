from rest_framework import serializers
from accounts.serializers import AccountSerializer
from persons.serializers import PersonSerializer, AchievementSerializer, HealthSerializer
from school.serializers import ClassroomSerializer, CourseSerializer

from .models import Student, Grade, Parent, Conduct
from school.models import Classroom, Course

from students.utils import get_student
from persons.utils import create_person, update_person, create_health, update_health, assign_health
from accounts.utils import create_account, update_account
from school.utils import assign_classroom_by_id, get_classroom, get_course

import logging
logger = logging.getLogger(__name__)


class GradeSerializer(serializers.ModelSerializer):
    course_id = serializers.IntegerField()
    student_id = serializers.IntegerField()
    final_score = serializers.SerializerMethodField(allow_null=True)
    class Meta:
        model = Grade
        fields = ['id', 'course_id', 'school_year', 'semester', 'quiz1', 'quiz2', 'quiz3', 'test', 'mid_term_test', 'final_test', 'start_update', 'student_id', 'final_score']

    def validate_course_id(self, value):
        try:
            Course.objects.get(pk=value)
            return value
        except Course.DoesNotExist:
            raise serializers.ValidationError('Course does not exist')

    def create(self, validated_data):
        course = get_course(validated_data.pop('course_id'))
        student = get_student(validated_data.pop('student_id'))
        return Grade.objects.create(course=course, student=student, **validated_data)

    def get_final_score(self, obj):
        quiz1 = obj.quiz1
        quiz2 = obj.quiz2
        quiz3 = obj.quiz3
        test = obj.test
        mid_term_test = obj.mid_term_test
        final_test = obj.final_test
        total = 4
        if quiz1 and test and mid_term_test and final_test:
            if quiz2:
                total += 1
            if quiz3:
                total += 1
            return round((quiz1 + quiz2 + quiz3 + test + mid_term_test * 2 + final_test * 2) / total, 2)



class ConductSerializer(serializers.ModelSerializer):
    student_id = serializers.IntegerField()
    class Meta:
        model = Conduct
        fields = ['id', 'score', 'semester', 'school_year', 'student_id']


class StudentParentSerializer(serializers.ModelSerializer):
    person = PersonSerializer()
    classroom = ClassroomSerializer()
    class Meta:
        model = Student
        fields = '__all__'

class ParentSerializer(serializers.ModelSerializer):
    person = PersonSerializer()
    student_id = serializers.PrimaryKeyRelatedField(source='students', many=True, queryset=Student.objects.all(), write_only=True)
    students = StudentParentSerializer(read_only=True, many=True)

    class Meta:
        model = Parent
        fields = ['id', 'person', 'student_id', 'avacation', 'students']

    def create(self, validated_data):
        logger.error(validated_data)
        person = create_person(validated_data.pop('person'))
        parent = Parent.objects.create(person=person, avacation=validated_data.pop('avacation'))
        for student in validated_data.pop('students'):
            parent.students.add(student)

        parent.save()
        return parent

    def update(self, instance, validated_data):
        try:
            update_person(instance.person, validated_data.pop('person'))
        except KeyError:
            pass

        instance.students.clear()
        for student in validated_data.pop('students'):
            instance.students.add(student)

        instance.save()
        return instance


class StudentSerializer(serializers.ModelSerializer):
    account = AccountSerializer()
    person = PersonSerializer()
    health = HealthSerializer(required=False, allow_null=True)
    classroom_id = serializers.IntegerField()
    parents = ParentSerializer(many=True, read_only=True)

    class Meta:
        model = Student
        fields = ['id', 'account', 'person', 'classroom_id', 'admission_year', 'health', 'status', 'parents']

    def create(self, validated_data):
        person_model = create_person(validated_data.pop('person'))
        account_model = create_account(validated_data.pop('account'))
        try:
            student = Student.objects.create(account=account_model,
                                             person=person_model,
                                             **validated_data)
        except Exception:
            raise serializers.ValidationError('Something wrong with your student information')

        try:
            create_health(validated_data.pop('health'))
        except KeyError:
            pass

        student.save()
        return student

    def update(self, instance, validated_data):
        try:
            update_account(instance.account, validated_data.pop('account'))
        except KeyError:
            pass

        try:
            update_person(instance.person, validated_data.pop('person'))
        except KeyError:
            pass

        try:
            if instance.health is None:
                health = create_health(validated_data.pop('health'))
                assign_health(instance, health)
            else:
                update_health(student, validated_data.pop('health'))
        except:
            pass

        instance.classroom_id = validated_data.get('classroom_id', instance.classroom_id)
        instance.status = validated_data.get('status', instance.status)
        instance.admission_year = validated_data.get('admission_year', instance.admission_year)
        instance.save()
        return instance

