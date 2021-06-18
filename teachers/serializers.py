from rest_framework import serializers
from .models import Teacher
from school.models import Classroom
from accounts.serializers import AccountSerializer
from persons.serializers import PersonSerializer, AchievementSerializer, HealthSerializer
from persons.utils import create_person, update_person
from accounts.utils import create_account, update_account


class TeacherSerializer(serializers.ModelSerializer):
    account = AccountSerializer()
    person = PersonSerializer()
    achievements = AchievementSerializer(required=False, allow_null=True, many=True)

    class Meta:
        model = Teacher
        fields = ['id', 'account', 'person', 'achievements', 'home_class']
        extra_kwargs = {'home_class': {'required': False}}

    def create(self, valiated_data):
        person_model = create_person(valiated_data.pop('person'))
        account_model = create_account(valiated_data.pop('account'))

        try:
            teacher = Teacher.objects.create(account=account_model, person=person_model, **valiated_data)
        except Exception:
            raise serializers.ValidationError('Something wrong with your teacher information')

        return teacher

    def update(self, instance, valiated_data):
        try:
            update_person(instance.person, valiated_data.pop('person'))
        except KeyError:
            pass

        try:
            update_account(instance.account, valiated_data.pop('account'))
        except KeyError:
            pass

        instance.save()
        return instance
