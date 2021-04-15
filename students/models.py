import uuid
from django.db import models
from accounts.models import Account
from persons.models import PersonInfo, Health, Achievement
from school.models import Classroom, Course


class Student(models.Model):
    student_id = models.OneToOneField(PersonInfo, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name='students')
    health = models.ForeignKey(Health, on_delete=models.CASCADE)
    achievements = models.ManyToManyField(Achievement, related_name='students', db_table='student_archivement')
    status = models.CharField(max_length=64)
    admission_year = models.SmallIntegerField()
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='student')

    class Meta:
        db_table = 'student'


class Parent(models.Model):
    parent_id = models.OneToOneField(PersonInfo, on_delete=models.CASCADE)
    avacation = models.CharField(max_length=128)

    class Meta:
        db_table = 'parent'


class Grade(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='grades')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='grades')
    school_year = models.SmallIntegerField()
    term = models.SmallIntegerField()
    quiz1 = models.DecimalField(max_digits=3, decimal_places=2)
    quiz2 = models.DecimalField(max_digits=3, decimal_places=2, null=True)
    quiz3 = models.DecimalField(max_digits=3, decimal_places=2, null=True)
    test = models.DecimalField(max_digits=3, decimal_places=2)
    mid_term_test = models.DecimalField(max_digits=3, decimal_places=2)
    final_test = models.DecimalField(max_digits=3, decimal_places=2)
    start_update = models.DateTimeField()

    class Meta:
        db_table = 'grade'


class Conduct(models.Model):
    id = models.AutoField(primary_key=True)
    score = models.CharField(max_length=32)
    term = models.SmallIntegerField()
    school_year = models.SmallIntegerField()
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='conduct')

    class Meta:
        db_table = 'conduct'
