from django.urls import path
from .views import *

urlpatterns = [
    path('students', StudentListView.as_view()),
    path('teachers', TeacherListView.as_view()),
    path('set_password/<username>', SetPasswordView.as_view()),
]
