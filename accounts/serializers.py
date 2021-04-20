from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.authtoken.models import Token

user = get_user_model()


class AccountSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=128, required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate_username(self, value):
        try:
            account = user.objects.get(username=value)
        except user.DoesNotExist:
            raise serializers.ValidationError('Username not found')
        return account


class AuthAccountSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()

    class Meta:
        model = user
        fields = ['username', 'is_admin', 'token']

    def get_token(self, obj):
        if Token.objects.get(user=obj):
            return Token.objects.get(user=obj).key
        return Token.objects.create(user=obj).key
