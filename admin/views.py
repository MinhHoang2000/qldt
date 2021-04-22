from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework import status, serializers
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import SetPasswordSerializer


class SetPasswordView(APIView):
    permission_classes = (IsAdminUser, IsAuthenticated)

    def post(self, request, username):
        account = SetPasswordSerializer(data=request.data)
        try:
            account.is_valid(raise_exception=True)
            user = get_user_model().objects.get(username=username)
            user.set_password(account.validated_data['new_password'])
            user.save()
        except serializers.ValidationError:
            return Response(account.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_200_OK)
