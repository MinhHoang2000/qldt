from django.urls import path
from .views import LoginView

urlpatterns = [
    path('api/v1/login', LoginView.as_view())
]
