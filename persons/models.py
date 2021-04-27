import uuid
from django.db import models
from django.utils import timezone

GENDERS = [('M', 'Nam'),
           ('F', 'Nu')]


class PersonInfo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    gender = models.CharField(max_length=1, choices=GENDERS)
    date_of_birth = models.DateField()
    address = models.CharField(max_length=128)
    ethnicity = models.CharField(max_length=32, null=True)
    religion = models.CharField(max_length=32, null=True)
    phone_number = models.CharField(max_length=11, null=True)

    class Meta:
        db_table = 'person_info'

    def __str__(self):
        return self.last_name + ' ' + self.first_name


class Achievement(models.Model):
    id = models.AutoField(primary_key=True)
    achievement_name = models.CharField(max_length=128)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'achievement'


class Health(models.Model):
    id = models.AutoField(primary_key=True)
    height = models.SmallIntegerField()
    weight = models.SmallIntegerField()
    eye_sight = models.SmallIntegerField()
    health_status = models.TextField(null=True)
    disease = models.TextField(null=True)

    class Meta:
        db_table = 'health'
