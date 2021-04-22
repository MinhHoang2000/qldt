from django.urls import path
from .views import *

urlpatterns = [
    path('login', LoginView.as_view()),
    path('register', RegisterView.as_view()),
    path('change_password', ChangePasswordView.as_view()),
    path('set_password/<username>', SetPasswordView.as_view()),
]
