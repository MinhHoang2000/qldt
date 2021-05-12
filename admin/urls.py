from django.urls import path
from .views import *

urlpatterns = [
    # admin account
    path('update', UpdateView.as_view()),
    path('register', RegisterView.as_view()),

    # account
    path('accounts', AccountView.as_view()),
    path('permissions', PermissionView.as_view()),

    # student
    path('students', StudentView.as_view()),
    path('students/grades', StudentGradeView.as_view()),

    # parent
    path('parents', ParentView.as_view()),

    # teacher
    path('teachers', TeacherView.as_view()),

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
    path('achievements', AchievementView.as_view()),
    path('achievements/students', StudentAchievementView.as_view()),
    path('achievements/teachers', TeacherAchievementView.as_view()),
]
