from django.db import models
from accounts.models import Account
from teachers.models import Teacher
from datetime import datetime
import os

DAY_OF_WEEK = [('Mon', 'Monday'),
               ('Tue', 'Tuesday'),
               ('Wed', 'Wednesday'),
               ('Thu', 'Thusday'),
               ('Fri', 'Friday'),
               ('Sat', 'Satuday'),
               ('Sun', 'Sunday')]

CHOICES_SHIFT = (
        ("M1", "7:15-8:00"),
        ("M2", "8:10-8:55"),
        ("M3", "9:05-9:50"),
        ("M4", "10:05-10:50"),
        ("M5", "11:00-11:45"),
        ("A1", "13:00-13:45"),
        ("A2", "13:55-14:10"),
        ("A3", "14:50-15:35"),
        ("A4", "15:50-16:35"),
        ("A5", "16:45-17:30"),
    )

CHOICES_DAY_NEW = [(2, 'Monday'),
               (3, 'Tuesday'),
               (4, 'Wednesday'),
               (5, 'Thusday'),
               (6, 'Friday'),
               (7, 'Saturday'),
               (8, 'Sunday')]

GROUP_COURSE = (
        ("Sc", "Science"),
        ("So", "Society"),
        ("Ph", "Physical"),
    )

CLASSIFICATION = (
    ("A", "Excellent"),
    ("B", "Good"),
    ("C", "Quite good"),
    ("D", "Not good"),
    ("F", "Fail"),
)

DEVICE_STATUS = [('N', 'Normal'),
                 ('B', 'Broken'),
                 ('O', 'Old'), ]


class Course(models.Model):
    id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=32)
    group_course = models.CharField(max_length=2, choices=GROUP_COURSE)

    class Meta:
        db_table = 'course'

    def __str__(self):
        return self.course_name

class Classroom(models.Model):
    id = models.AutoField(primary_key=True)
    class_name = models.CharField(max_length=8)
    homeroom_teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='home_class', null=True)
    location = models.CharField(max_length=16)

    class Meta:
        db_table = 'classroom'

    def __str__(self):
        return self.class_name


class Timetable(models.Model):
    id = models.AutoField(primary_key=True)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name='timetables')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='timetables')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='timetables')
    day_of_week = models.CharField(max_length=3, choices=DAY_OF_WEEK)
    shifts = models.SmallIntegerField()
    semester = models.SmallIntegerField(default=1)
    school_year = models.SmallIntegerField()

    class Meta:
        db_table = 'timetable'


class ClassRecord(models.Model):
    id = models.AutoField(primary_key=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='classrecords')
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name='classrecords')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='classrecords')
    classification = models.CharField(max_length=1, choices=CLASSIFICATION, default='A')
    study_week = models.SmallIntegerField()
    attendant = models.SmallIntegerField()
    note = models.TextField(null=True)
    day_of_week = models.CharField(max_length=3, choices=DAY_OF_WEEK)
    shifts = models.SmallIntegerField()
    semester = models.SmallIntegerField(default=1)
    school_year = models.SmallIntegerField()

    class Meta:
        db_table = 'class_record'


class Device(models.Model):
    id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=1, choices=DEVICE_STATUS, default='N')
    device_name = models.CharField(max_length=128)
    amount = models.IntegerField()
    price = models.IntegerField()

    class Meta:
        db_table = 'device'


class DeviceManage(models.Model):
    id = models.AutoField(primary_key=True)
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='device_manages')
    day_of_week = models.CharField(max_length=3, choices=DAY_OF_WEEK)
    shifts = models.SmallIntegerField()
    week = models.SmallIntegerField()
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='devices')

    class Meta:
        db_table = 'device_manage'


def teacher_directory_path(instance, filename):
    now = datetime.now()
    year = now.year
    month = now.month
    day = now.day
    return f'{instance.teacher.id }-{instance.teacher.person.first_name}_{instance.teacher.person.last_name}/{instance.classroom.id}-{instance.classroom.class_name}/{instance.course.course_name}/{year}-{month}-{day}/{filename}'


class StudyDocument(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128)
    file = models.FileField(upload_to=teacher_directory_path)
    study_week = models.SmallIntegerField()
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='files')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='files')
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = "study_document"

    # def delete(self, *args, **kwargs):
    #     os.remove(os.path.join(settings.MEDIA_ROOT, self.file.name))
    #     super(StudyDocument,self).delete(*args, **kwargs)

class TeachingInfo(models.Model):
    id = models.AutoField(primary_key=True)
    school_year = models.CharField(max_length=250)
    semester = models.SmallIntegerField()
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    class Meta:
        db_table = "teaching_information"
