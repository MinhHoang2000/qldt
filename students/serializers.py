from rest_framework import serializers
from accounts.serializers import AccountSerializer
from persons.serializers import PersonSerializer, AchievementSerializer, HealthSerializer
from school.serializers import ClassroomSerializer
from .models import Student
from school.models import Classroom
from persons.utils import *
from accounts.utils import *
from school.utils import *

import logging
logger = logging.getLogger(__name__)


class StudentSerializer(serializers.ModelSerializer):
    classroom_id = serializers.IntegerField()
    account = AccountSerializer()
    person = PersonSerializer()
    achievements = AchievementSerializer(required=False, allow_null=True, many=True)
    health = HealthSerializer(required=False, allow_null=True)

    class Meta:
        model = Student
        fields = ['id', 'account', 'person', 'classroom_id', 'admission_year', 'health', 'status', 'achievements']

    def create(self, validated_data):
        person_model = create_person(validated_data.pop('person'))
        account_model = create_account(validated_data.pop('account'))
        classroom_model = get_classroom(validated_data.pop('classroom_id'))

        try:
            student = Student.objects.create(account=account_model,
                                             person=person_model,
                                             classroom=classroom_model,
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
            update_person(instance.person, validated_data.pop('person'))
            assign_classroom_by_id(instance, validated_data.pop('classroom_id'))

            if instance.health is None:
                health = create_health(validated_data.pop('health'))
                assign_health(instance, health)
            else:
                update_health(student, validated_data.pop('health'))
        except KeyError:
            pass

        instance.status = validated_data.get('status', instance.status)
        instance.admission_year = validated_data.get('admission_year', instance.admission_year)
        instance.save()

        return instance
