from rest_framework import serializers
from .utils import get_classroom
from .models import Timetable, ClassRecord
from teachers.utils import get_teacher


def validate_teacher_timetable(teacher_id, day_of_week, shifts):
    teacher = get_teacher(teacher_id)
    timetable = Timetable.objects.filter(teacher=teacher,
                                         day_of_week=day_of_week,
                                         shifts=shifts)
    if timetable.exists():
        raise serializers.ValidationError(f'Teacher timetable conflicts at {day_of_week} | {shifts}')


def validate_classroom_timetable(classroom_id, day_of_week, shifts):
    classroom = get_classroom(classroom_id)
    timetable = Timetable.objects.filter(classroom=classroom,
                                         day_of_week=day_of_week,
                                         shifts=shifts)
    if timetable.exists():
        raise serializers.ValidationError(f'Classroom timetable conflicts at {day_of_week} | {shifts}')


def validate_classroom_record(classroom_id, day_of_week, shifts, study_week):
    classroom = get_classroom(classroom_id)
    record = ClassRecord.objects.filter(classroom=classroom,
                                        day_of_week=day_of_week,
                                        shifts=shifts, study_week=study_week)
    if record.exists():
        raise serializers.ValidationError(f'Classroom record conflicts at Week: {study_week} | {day_of_week} | {shifts}')


def validate_classroom_attendant(classroom_id, attendant):
    classroom = get_classroom(classroom_id)
    if attendant > classroom.students.count():
        raise serializers.ValidationError('Attendant can\'t be larger than total student')
