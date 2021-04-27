from rest_framework import serializers
from django.contrib.auth import password_validation


class SetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True, write_only=True)

    def validate_new_password(self, value):
        password_validation.validate_password(value)
        return value
