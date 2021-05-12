from django.urls import path
from .views import *

urlpatterns = [
    # admin account
    path('update', UpdateView.as_view()),
    path('register', RegisterView.as_view()),

    # account
    path('accounts', AccountView.as_view()),
    path('accounts/permissions', PermissionView.as_view()),

    # student
    path('students', StudentView.as_view()),
    path('students/<int:pk>/grades', StudentGradeListView.as_view()),
    path('students/<int:student_pk>/grades/<int:grade_pk>', StudentGradeDetailView.as_view()),

    # parent
    path('parents', ParentListView.as_view()),
    path('parents/<int:pk>', ParentDetailView.as_view()),

    # teacher
    path('teachers', TeacherListView.as_view()),
    path('teachers/<int:pk>', TeacherDetailView.as_view()),

    # classroom
    path('classrooms', ClassroomListView.as_view()),
    path('classrooms/<int:pk>', ClassroomDetailView.as_view()),
    path('classrooms/<int:pk>/timetables', ClassTimetableView.as_view()),
    path('classrooms/<int:class_pk>/timetables/<int:timetable_pk>', ClassTimetableDetailView.as_view()),
    path('classrooms/<int:pk>/records', ClassRecordView.as_view()),
    path('classrooms/<int:class_pk>/records/<record_pk>', ClassRecordDetailView.as_view()),

    # course
    path('courses', CourseView.as_view()),

    # achievements
    path('achievements', AchievementListView.as_view()),
    path('achievements/<int:pk>', AchievementDetailView.as_view()),
    path('achievements/students', StudentAchievementListView.as_view()),
    path('achievements/students/<int:pk>', StudentAchievementDetailView.as_view()),
    path('achievements/teachers', TeacherAchievementListView.as_view()),
    path('achievements/teachers/<int:pk>', TeacherAchievementDetailView.as_view()),
]

{
    "person": {
        "first_name": "Tham lam",
        "last_name": "Ngu dot",
        "gender": "M",
        "date_of_birth": "2000-01-01",
        "address": "ui23g2ui"
    },
    "account": {
        "username": "t1",
        "password": "hailong123"
    },
    "admission_year": 2018,
    "status": "DH"
}
