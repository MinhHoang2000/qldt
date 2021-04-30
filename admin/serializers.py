from rest_framework import serializers
from django.contrib.auth import password_validation

from persons.serializers import AchievementSerializer


class SetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True, write_only=True)

    def validate_new_password(self, value):
        password_validation.validate_password(value)
        return value


class StudentAchievementSerializer(serializers.Serializer):
    student_id = serializers.IntegerField()
    achievements = AchievementSerializer(many=True)

    def create(self, validated_data):
        student = get_student(validated_data.pop('student_id'))
        achievement = create_achievenment(validated_data.pop('achievement'))

        student.achievements.add(achievement)
        student.save()

        return student
