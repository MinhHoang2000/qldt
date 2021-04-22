from django.contrib.auth import get_user_model, password_validation
from rest_framework import serializers
from rest_framework.authtoken.models import Token

user = get_user_model()


class AuthAccountSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()

    class Meta:
        model = user
        fields = ['username', 'is_admin', 'token']

    def get_token(self, obj):
        if Token.objects.filter(user=obj):
            return Token.objects.get(user=obj).key
        return Token.objects.create(user=obj).key


class AccountRegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=128, required=True)
    password = serializers.CharField(required=True, write_only=True)
    email = serializers.CharField()

    def validate_username(self, value):
        account = user.objects.filter(username=value)
        if account.exists():
            raise serializers.ValidationError('This username is already taken')
        return value

    def validata_password(sefl, value):
        password_validation.validate_password(value)
        return value

    def create(self, validated_data):
        return user.objects.create(**validated_data)


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
