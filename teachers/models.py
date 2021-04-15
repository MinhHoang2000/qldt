import uuid
from django.db import models
from persons.models import PersonInfo, Archivement
from accounts.models import Account


class Teacher(models.Model):
    id = models.ForeignKey(primary_key=True, PersonInfo, on_delete=models.CASCADE)
    archivements = models.ManyToManyField(Archivement, related_name='teachers', db_table='teacher_archivement')
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='teacher_account')

    class Meta:
        db_table = 'teacher'
