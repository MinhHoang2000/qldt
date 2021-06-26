from django.db import models
from accounts.models import Account
from persons.models import PersonInfo, Health, Achievement
from school.models import Classroom, Course

LEARNING_STATUS = [('DH', 'Dang hoc'),
                   ('DT', 'Dinh chi hoc'),
                   ('TH', 'Thoi hoc')]

SCORES = [('T', 'Tot'),
          ('K', 'Kha'),
          ('TB', 'Trung binh'),
          ('Y', 'Yeu')]


class Student(models.Model):

    id = models.AutoField(primary_key=True)
    person = models.OneToOneField(PersonInfo, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name='students')
    health = models.ForeignKey(Health, on_delete=models.CASCADE, null=True)
    achievements = models.ManyToManyField(Achievement, related_name='students', db_table='student_archivement')
    status = models.CharField(max_length=2, choices=LEARNING_STATUS, null=True)
    admission_year = models.SmallIntegerField()
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='student', null=True)

    class Meta:
        db_table = 'student'

    def __str__(self):
        return self.person.__str__()


class Parent(models.Model):
    person = models.OneToOneField(PersonInfo, on_delete=models.CASCADE)
    avacation = models.CharField(max_length=128)
    students = models.ManyToManyField(Student, related_name='parents', db_table='parent_student')

    class Meta:
        db_table = 'parent'

    def __str__(self):
        return self.person.__str__()


class Grade(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='grades')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='grades')
    school_year = models.SmallIntegerField()
    semester = models.SmallIntegerField()
    quiz1 = models.DecimalField(max_digits=3, decimal_places=2, null=True)
    quiz2 = models.DecimalField(max_digits=3, decimal_places=2, null=True)
    quiz3 = models.DecimalField(max_digits=3, decimal_places=2, null=True)
    test = models.DecimalField(max_digits=3, decimal_places=2, null=True)
    mid_term_test = models.DecimalField(max_digits=3, decimal_places=2, null=True)
    final_test = models.DecimalField(max_digits=3, decimal_places=2, null=True)
    start_update = models.DateTimeField(null=True)

    class Meta:
        db_table = 'grade'


class Conduct(models.Model):
    id = models.AutoField(primary_key=True)
    score = models.CharField(max_length=2, choices=SCORES, null=True)
    semester = models.SmallIntegerField()
    school_year = models.SmallIntegerField()
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='conduct')

    class Meta:
        db_table = 'conduct'
