from django.urls import path
from .views import SetPasswordView

urlpatterns = [
    path('set_password/<username>', SetPasswordView.as_view()),
]
