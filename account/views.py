from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import *

class VUserRegistrationView(APIView):
    def post(self, request, format=None):

        serializer = VUserRegisterationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            return Response({'msg': 'Registration Successful'}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class OUserRegistrationView(APIView):
    def post(self, request, format=None):

        serializer = OUserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            return Response({'msg': 'Registration Successful'}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)