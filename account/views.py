from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.exceptions import ObjectDoesNotExist
from account.renderers import UserRenderer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from .models import *
from .utils import Util
from django.contrib.auth import get_user_model


def get_tokens_for_user(user):  # Generate token manually
    refresh = RefreshToken.for_user(user)

    return {
        'refresh' : str(refresh),
        'access' : str(refresh.access_token),
    }

#Signup Classes


class VUserRegistrationView(APIView):   # Volunteer Registration
    renderer_classes = [UserRenderer]
    def post(self, request, format=None):

        serializer = VUserRegisterationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response({'msg': 'Registration Successful', 'token' : f'{token}', 'as' : 'volunteer'}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class OUserRegistrationView(APIView):   # Organization Registration
    renderer_classes = [UserRenderer]
    def post(self, request, format=None):

        serializer = OUserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response({'msg': 'Registration Successful', 'token' : f'{token}', 'as' : 'organization'}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):   # Login
    renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')

            try:
                # Retrieve the user object using the email address
                user = CustomUser.objects.get(email=email) 
             
         
                username = user.username
                # Authenticate the user using the retrieved username and provided password
                user = authenticate(username=username, password=password)

                if user is not None:
                    token = get_tokens_for_user(user)
                    if user.is_volunteer is True:
                        uas = 'volunteer'
                    elif user.is_organization is True:
                        uas = 'organization'
                    else:
                        uas = 'staff'
                    
                    return Response({'msg':'Login Successful', 'token' : f'{token}', 'as' : f'{uas}'}, status = status.HTTP_200_OK)
                else:
                    return Response({'errors': {'non_field_errors':['email or Password is not valid']}}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                print(e)
                return Response({'errors': {'email_field_error':['Email not found']}}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

class UserChangePasswordView(APIView):  # Change password
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        serializer = UserChangePasswordSerializer(data=request.data, context={'user':request.user})
        if serializer.is_valid(raise_exception= True):
            return Response({'msg' : 'Password Changed Successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SendPasswordResetEmailView(APIView):  # Send Password Reset Email
    renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        host = request.get_host()
        serializer = SendPasswordResetEmailSerializer(data=request.data, context={'host': host})
        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data.get('email')
            try:
                user = CustomUser.objects.get(email=email)
                
                return Response({'msg' : 'Password Reset Email Sent'}, status=status.HTTP_200_OK)
            except Exception as e:
                print(e)
                return Response({'errors': {'email_field_error':['Email not found']}}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserPasswordResetView(APIView):  # Password Reset
    renderer_classes = [UserRenderer]
    def post(self, request, uid, token, format=None):
        serializer = UserPasswordResetSerializer(data=request.data, context={'uid':uid, 'token':token})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg' : 'Password Reset Successful'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SendConfirmationEmailView(APIView):  # Send Confirmation Email
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        host = request.get_host()

        try:
            user = request.user
            if user.is_volunteer is True:
                uas = 'volunteer'
            elif user.is_organization is True:
                uas = 'organization'
            else:
                uas = 'staff'
            uid = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            link = f"http://{host}/api/user/activate-email/{uid}/{token}"
            body = f"Hi,\nAn account as {uas} is created on our website.\nClick the link below to confirm your email:\n{link}\nIf it's not you then please ignore."
            data = {'email_body':  body, 'to_email': user.email, 'email_subject': 'Reset your password'}
            Util.send_email(data)
            return Response({'msg' : 'Confirmation Email Sent'}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class ActivateUserView(APIView):
    def get(self, request, uid, token, format=None):
        try:
            id = smart_bytes(urlsafe_base64_decode(uid))
            user = get_user_model().objects.get(id=id)
            if PasswordResetTokenGenerator().check_token(user, token):
                user.is_active = True
                user.save()
                return Response({'msg': 'Account activated successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Activation failed'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


