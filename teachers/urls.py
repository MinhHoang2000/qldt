# from os import name
from django.urls import path
from .views import TeachingInfoView, StudentView, StudentGradeView, ClassRecordView, StudyDocumentView, UploadStudyDocumentView, TimetableView, ClassTimetableView, StudentConductView

urlpatterns = [
    path('teaching_info', TeachingInfoView.as_view(), name='teaching_information'),

    path('class/<int:class_id>/students', StudentView.as_view(), name='list_student_of_class'),

    path('class/<int:class_id>/grades',StudentGradeView.as_view(), name='list_student_grade_of_class'),
    path('classes/timetable', ClassTimetableView.as_view()),
    path('classes/conduct', StudentConductView.as_view()),

    path('classes/<int:class_id>/records', ClassRecordView.as_view(), name='list_classrecord'),

    path('documents',StudyDocumentView.as_view(), name='list_study_document'),
    path('upload', UploadStudyDocumentView.as_view(), name='upload_study_document'),

    path('timetable', TimetableView.as_view(), name='teacher_timetable'),
]
