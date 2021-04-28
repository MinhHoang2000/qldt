from django.urls import path
from .views import *

urlpatterns = [
    path('update', UpdateView.as_view()),
    path('register', RegisterView.as_view()),
    path('accounts', AccountListView.as_view()),
    path('students', StudentListView.as_view()),
    path('students/<int:pk>', StudentDetailView.as_view()),
    path('teachers', TeacherListView.as_view()),
    path('teachers/<int:pk>', TeacherDetailView.as_view()),
    path('classrooms', ClassroomListView.as_view()),
    path('classrooms/<int:pk>', ClassroomDetailView.as_view()),
]
