from .serializers import PersonSerializer


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
