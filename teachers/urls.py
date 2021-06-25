# from os import name
from django.urls import path
from .views import TeachingInfoView, StudentView, StudentGradeView, ClassRecordView, StudyDocumentView, UploadStudyDocumentView, TimetableView, ClassTimetableView, StudentConductView, DeviceView, DeviceManageView, TeacherView

urlpatterns = [

    path('info', TeacherView.as_view()),
    path('teaching_info', TeachingInfoView.as_view(), name='teaching_information'),

    path('classes/<int:class_id>/students', StudentView.as_view(), name='list_student_of_class'),
    path('classes/<int:class_id>/grades',StudentGradeView.as_view(), name='list_student_grade_of_class'),
    path('classes/<int:class_id>/records', ClassRecordView.as_view(), name='list_classrecord'),

    path('class/conduct', StudentConductView.as_view()),
    path('class/timetable', ClassTimetableView.as_view()),

    path('documents',StudyDocumentView.as_view(), name='list_study_document'),
    path('upload', UploadStudyDocumentView.as_view(), name='upload_study_document'),
    path('device_manage', DeviceManageView.as_view()),
    path('devices', DeviceView.as_view()),

    path('timetable', TimetableView.as_view(), name='teacher_timetable'),
]
