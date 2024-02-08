from django.urls import path, include
from .views import *
urlpatterns = [
    path('volunteer_register/', VUserRegistrationView.as_view(), name = 'Vregister'),
    path('organization_register/', OUserRegistrationView.as_view(), name = 'Oregister'),
    path('login/', UserLoginView.as_view(), name = 'login'),
    path('changepassword/', UserChangePasswordView.as_view(), name = 'changepassword'),
    path('send-reset-password-email/', SendPasswordResetEmailView.as_view(), name = 'send-reset-password-email'),
    path('reset-password/<uid>/<token>/', UserPasswordResetView.as_view(), name = 'reset-password'),
]