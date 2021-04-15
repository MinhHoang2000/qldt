from django.db import models
from django.utils import timezone
from accounts.models import Account
from teachers.models import Teacher


class Course(models.Model):
    id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=32)

    class Meta:
        db_table = 'course'


class Classroom(models.Model):
    id = models.AutoField(primary_key=True)
    class_name = models.CharField(max_length=8)
    homeroom_teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='home_class')
    location = models.CharField(max_length=32)

    class Meta:
        db_table = 'classroom'


class Timetable(models.Model):
    id = models.AutoField(primary_key=True)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name='timetables')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='timetables')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='timetables')
    day_of_week = models.SmallIntegerField()
    shift = models.SmallIntegerField()

    class Meta:
        db_table = 'timetable'


class ClassRecord(models.Model):
    id = models.AutoField(primary_key=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='classrecords')
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name='classrecords')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='classrecords')
    study_week = models.SmallIntegerField()
    attendant = models.SmallIntegerField()
    note = models.TextField()
    day_of_week = models.SmallIntegerField()
    shift = models.SmallIntegerField()

    class Meta:
        db_table = 'class_record'


class Device(models.Model):
    id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=64)
    device_name = models.CharField(max_length=128)
    class Meta:
        db_table = 'device'

class DeviceManage(models.Model):
    id = models.AutoField(primary_key=True)
    day_of_week = models.SmallIntegerField()
    shift = models.SmallIntegerField()
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='devices')

    class Meta:
        db_table = 'device_manage'

class FileManage(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128)
    file = models.FileField()
    study_week = models.SmallIntegerField()
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='files')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='files')

    class Meta:
        db_table = 'file_manage'
