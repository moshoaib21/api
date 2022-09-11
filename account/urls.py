from django.contrib import admin
from django.urls import path, include
from account.views import UserLogin, UserPasswordResendEmail, UserRegistrationView,UserProfileView,UserChangePassword,UserPasswordResendEmail

urlpatterns = [
    path('register/', UserRegistrationView.as_view(),name='register'),
    path('login/', UserLogin.as_view(),name='login'),
    path('profile/', UserProfileView.as_view(),name='profile'),            
    path('UserChangePassword/', UserChangePassword.as_view(),name='UserChangePassword'),            
    path('user-password-resend-email/', UserPasswordResendEmail.as_view(),name='UserPasswordResendEmail'),            


]
