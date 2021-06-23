from django.contrib.auth import get_user_model, password_validation
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Permission
from students.models import Student
from teachers.models import Teacher
from persons.utils import update_person
from persons.serializers import PersonSerializer
user = get_user_model()


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = user
        fields = ['id', 'username', 'email', 'is_admin', 'password']
        extra_kwargs = {'email': {'required': False}, 'password': {'write_only': True}}

    def create(self, validated_data):
        if self.context.get('is_admin', False):
            return user.objects.create_superuser(**validated_data)
        return user.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        try:
            password = validated_data.pop('password')
            instance.set_password(password)
        except KeyError:
            pass

        instance.save()
        return instance

    def validate_email(self, value):
        try:
            validate_email(value)
        except ValidationError:
            raise serializers.ValidationError('Your email format is wrong')
        return value

    def validate_username(self, value):
        account = user.objects.filter(username=value)
        if account.exists():
            raise serializers.ValidationError('This username is already taken')
        return value

    def validate_password(self, value):
        try:
            password_validation.validate_password(value)
        except ValidationError:
            raise serializers.ValidationError('Your password is not strong enough')
        return value


class AuthAccountSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()

    class Meta:
        model = user
        fields = ['token']

    def get_token(self, user):
        refresh = RefreshToken.for_user(user)
        refresh['username'] = user.username

        if user.student.exists():
            refresh['account_type'] = 'student'
        elif user.teacher.exists():
            refresh['account_type'] = 'teacher'
        elif user.is_admin:
            refresh['account_type'] = 'admin'
        else:
            refresh['account_type'] = 'none'
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)

    def validate_current_password(self, value):
        if self.context['request'].user.check_password(value):
            return value
        else:
            raise serializers.ValidationError('Your current password is wrong')

    def validate_new_password(self, value):
        if self.context['request'].user.check_password(value):
            raise serializers.ValidationError('Your new password is the same to the current one')
        else:
            password_validation.validate_password(value)
        return value


class StudentProfileSerializer(serializers.ModelSerializer):
    account_type = serializers.CharField(default='student')
    person = PersonSerializer()
    class Meta:
        model = Student
        fields = ['id', 'person', 'account_type']


    def update(self, instance, validated_data):
        try:
            update_person(instance.person, validated_data.pop('person'))
        except KeyError:
            pass

        instance.save()
        return instance


class TeacherProfileSerializer(serializers.ModelSerializer):
    account_type = serializers.CharField(default='teacher')
    person = PersonSerializer()
    class Meta:
        model = Teacher
        fields = ['id', 'person', 'account_type']

    def update(self, instance, validated_data):
        try:
            update_person(instance.person, validated_data.pop('person'))
        except KeyError:
            pass

        instance.save()
        return instance


class PermissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Permission
        fields = ['id', 'permission_name', 'permission_code']
