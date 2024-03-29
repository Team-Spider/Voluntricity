from django.utils.encoding import smart_bytes, smart_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework import serializers
from .models import CustomUser
from .utils import Util

class VUserRegisterationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'password', 'password2', 'tc']
        extra_kwargs = {
            'password' : {'write_only':True},
            'email' : {'required' : True},
            'tc' : {'required' : True},
        }

    #validation of password
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        email = attrs.get('email')
        if password != password2:
            raise serializers.ValidationError("Password Doesn't match")
        if CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email Already Exists")
        return attrs
    
    def create(slef, validate_data):
        validate_data['is_volunteer'] = True
        validate_data['name'] = None
        validate_data['is_active'] = False
        user = CustomUser.objects.create_user(**validate_data)
        return user
    
class OUserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
    
    class Meta:
        model = CustomUser
        fields = ['email', 'name', 'password', 'password2', 'tc']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True},
            'name': {'required': True},
            'tc' : {'required' : True},
        }

    # Validation of password
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        email = attrs.get('email')
        if password != password2:
            raise serializers.ValidationError("Passwords don't match")
        if CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email Already Exists")
        return attrs
    
    def create(self, validated_data):
        # Extract organization name from validated_data
        organization_name = validated_data.get('name', '')
        
        # Generate unique username from organization name
        username = self.generate_username(organization_name)
        
        # Add username to validated data
        validated_data['username'] = username

        validated_data['is_organization'] = True
        validated_data['first_name'] = None
        validated_data['last_name'] = None
        validated_data['is_active'] = False
        
        # Create user with the updated validated_data
        user = CustomUser.objects.create_user(**validated_data)
        
        return user

    def generate_username(self, organization_name):
        # Convert organization name to lowercase and replace spaces with underscores
        username = organization_name.lower().replace(' ', '_')
        
        # Check if username already exists, if so, add a number suffix
        suffix = 1
        while CustomUser.objects.filter(username=username).exists():
            username = f"{organization_name.lower().replace(' ', '_')}{suffix}"
            suffix += 1
        
        return username
    

class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length = 254)
    class Meta:
        model = CustomUser
        fields = ['email', 'password']

        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True},
        }


class UserChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length = 255, style={'input_type':'password'}, write_only=True)
    password2 = serializers.CharField(max_length = 255, style={'input_type':'password'}, write_only=True)
    class Meta:
        fields = ['password', 'password2']

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')
        if password != password2:
            raise serializers.ValidationError("Passwords don't match")
        user.set_password(password)
        user.save()
        return attrs


class SendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length = 254)
    class Meta:
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email')
        if not CustomUser.objects.filter(email=email).exists():
           print("lol")
           raise serializers.ValidationError("Email not found")
        else:
            user = CustomUser.objects.get(email=email)
            uid = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            host = self.context.get('host')
            link = f"http://{host}/reset/{uid}/{token}"

            # Send email with link
            body = f"Reset your password by clicking the link below:\n{link}"
            data = {'email_body':  body, 'to_email': user.email, 'email_subject': 'Reset your password'}
            Util.send_email(data)
        return attrs
    
class UserPasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(max_length = 255, style={'input_type':'password'}, write_only=True)
    password2 = serializers.CharField(max_length = 255, style={'input_type':'password'}, write_only=True)
    class Meta:
        fields = ['password', 'password2']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            password2 = attrs.get('password2')
            if password != password2:
                raise serializers.ValidationError("Passwords don't match")

            uid = self.context.get('uid')
            token = self.context.get('token')
            id = smart_str(urlsafe_base64_decode(uid))
            user = CustomUser.objects.get(id = id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise serializers.ValidationError("Token is not valid or has expired")
            user.set_password(password)
            user.save()
            return attrs
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user, token)
            raise serializers.ValidationError("Token is not valid or has expired")
