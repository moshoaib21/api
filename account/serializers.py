from base64 import urlsafe_b64decode
from dataclasses import fields
from lib2to3.pgen2 import token
from tkinter.ttk import Style
from unittest.util import _MAX_LENGTH
from xml.dom import ValidationErr
from xml.sax.handler import feature_external_ges
from rest_framework import serializers
from account.models import User
from django.utils.encoding import smart_str , force_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator


class UserRegistrationSerializer(serializers.ModelSerializer):
    password2=serializers.CharField(style={'inpu_type':'password'},write_only=True)
    class Meta:
        model= User
        fields=['email','name','password','passwod2','tc']
        fields = '__all__'
        extra_kwargs={
            'password':{'write_only':True}
        }
#view se jo data mila hai woh access hota hai attrs me
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2 :
            raise serializers.ValidationError("password and confirm password doesn't match ")
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=225)
    class Meta:
        model = User
        fields = ['email','password']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','email']

class UserChangePasswordSerializer(serializers.ModelSerializer):
    password =serializers.CharField(max_length=225,style={'input_type':'password'},write_only=True)
    password2 =serializers.CharField(max_length=225,style={'input_type':'password'},write_only=True)
    class Meta :
        model = User
        fields = ['password','password2']

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')
        if password != password2 :
            raise serializers.ValidationError("password and confirm password doesn't match ")
        user.set_password(password)
        user.save()
        return attrs

class UserPasswordResendEmailSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=225)
    class Meta:
        model = User
        fields=['email']
    def validate(self, attrs):
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            user=User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            print('Encode UID',uid)
            token = PasswordResetTokenGenerator().make_token(user)
            print('password Reset token ',token)
            link ='http://localhost:3000/api/user/reset/'+uid+'/'+token
            print('passwordReset link',link)
            return attrs
            # send Email code start here
        else:
            raise ValidationErr('You are not register user')


