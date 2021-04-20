from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from .serializers import AccountSerializer, AuthAccountSerializer
from django.contrib.auth import authenticate

class LoginView(APIView):

    def post(self, request):
        credential = JSONParser().parse(request)
        serializer = AccountSerializer(data=credential)
        try:
            serializer.is_valid()
        except:
            return Response(serializer.errors, status.HTTP_401_UNAUTHORIZED)
        account = authenticate(**credential)
        if account == None:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            data = AuthAccountSerializer(account).data
            return Response(data, status=status.HTTP_200_OK)
