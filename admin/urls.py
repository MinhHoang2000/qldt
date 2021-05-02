from django.urls import path
from .views import *

urlpatterns = [
    path('update', UpdateView.as_view()),
    path('register', RegisterView.as_view()),
    path('accounts', AccountListView.as_view()),

    # student
    path('students', StudentListView.as_view()),
    path('students/<int:pk>', StudentDetailView.as_view()),
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
    path('classrooms/<int:pk>/records', ClassRecordView.as_view()),

    # course
    path('courses', CourseListView.as_view()),
    path('courses/<int:pk>', CourseDetailView.as_view()),

    # achievements
    path('achievements', AchievementListView.as_view()),
    path('achievements/<int:pk>', AchievementDetailView.as_view()),
    path('achievements/students', StudentAchievementListView.as_view()),
    path('achievements/students/<int:pk>', StudentAchievementDetailView.as_view()),
    path('achievements/teachers', TeacherAchievementListView.as_view()),
    path('achievements/teachers/<int:pk>', TeacherAchievementDetailView.as_view()),
]
