from django.contrib.auth import get_user_model, password_validation
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from students.models import Student
from teachers.models import Teacher

user = get_user_model()


class AccountSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=128, required=True)
    password = serializers.CharField(required=True, write_only=True)
    email = serializers.CharField(required=False)

    def create(self, validated_data):
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

    def validate_password(sefl, value):
        try:
            password_validation.validate_password(value)
        except ValidationError:
            raise serializers.ValidationError('Your password is not strong enough')
        return value


class AuthAccountSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()

    class Meta:
        model = user
        fields = ['id', 'username', 'is_admin', 'token']

    def get_token(self, obj):
        if Token.objects.filter(user=obj):
            return Token.objects.get(user=obj).key
        return Token.objects.create(user=obj).key


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

    class Meta:
        model = Student
        fields = ['id', 'person', 'account_type']


class TeacherProfileSerializer(serializers.ModelSerializer):
    account_type = serializers.CharField(default='teacher')

    class Meta:
        model = Teacher
        fields = ['id', 'person', 'account_type']
