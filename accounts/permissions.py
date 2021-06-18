from rest_framework.permissions import BasePermission
from teachers.models import Teacher

class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_anonymous:
            return False
        return obj.account == request.user

class IsTeacher(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        return Teacher.objects.filter(account=user).exists()
