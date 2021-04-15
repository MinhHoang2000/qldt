from django.db import models
from persons.models import PersonInfo, Achievement
from accounts.models import Account


class Teacher(models.Model):
    person = models.OneToOneField(PersonInfo, on_delete=models.CASCADE)
    archivements = models.ManyToManyField(Achievement, related_name='teachers', db_table='teacher_archivement')
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='teacher_account', null=True)

    class Meta:
        db_table = 'teacher'

    def __str__(self):
        return person.__str__()
