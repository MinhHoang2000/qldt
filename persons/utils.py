from rest_framework import exceptions
from .serializers import PersonSerializer, HealthSerializer, AchievementSerializer
from .models import Achievement


def create_person(person_data):
    person_serializer = PersonSerializer(data=person_data)
    person_serializer.is_valid(raise_exception=True)
    return person_serializer.save()


def update_person(person, person_data):
    person_serializer = PersonSerializer(person, data=person_data, partial=True)
    person_serializer.is_valid(raise_exception=True)
    person_serializer.save()


def assign_health(student, health):
    student.health = health


def create_health(health_data):
    health_serializer = HealthSerializer(data=health_data)
    health_serializer.is_valid(raise_exception=True)
    return health_serializer.save()


def update_health(student, health_data):
    health_serializer = HealthSerializer(student.health, data=health_data, partial=True)
    health_serializer.is_valid(raise_exception=True)
    health_serializer.save()


def get_achievement(pk):
    try:
        return Achievement.objects.get(pk=pk)
    except Achievement.DoesNotExist:
        raise exceptions.NotFound('Student does not exist')


def create_achievement(achievement_data):
    achievement = AchievementSerializer(data=achievement_data)
    achievement.is_valid(raise_exception=True)
    return achievement.save()


def update_achievement(achievement, achievement_data):
    achievement_serializer = AchievementSerializer(achievement, data=achievement_data, partial=True)
    achievement_serializer.is_valid(raise_exception=True)
    achievement_serializer.save()


def delete_achievement(pk):
    return get_achievement(pk).delete()
