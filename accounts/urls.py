from django.urls import path
from .views import LoginView, RegisterView

urlpatterns = [
    path('api/v1/login/', LoginView.as_view()),
    path('api/v1/register/', RegisterView.as_view()),
]
