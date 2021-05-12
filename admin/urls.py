from django.urls import path
from .views import *
from .students import *

urlpatterns = [
    # admin account
    path('update', UpdateView.as_view()),
    path('register', RegisterView.as_view()),

    # account
    path('accounts', AccountView.as_view()),
    path('accounts/permissions', PermissionView.as_view()),

    # student
    path('students', StudentView.as_view()),
    path('students/grades', StudentGradeView.as_view()),

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
    path('achievements', AchievementView.as_view()),
    path('achievements/students', StudentAchievementListView.as_view()),
    path('achievements/students/<int:pk>', StudentAchievementDetailView.as_view()),
    path('achievements/teachers', TeacherAchievementListView.as_view()),
    path('achievements/teachers/<int:pk>', TeacherAchievementDetailView.as_view()),
]
