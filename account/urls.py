from django.urls import path, include
from .views import *
urlpatterns = [
    path('volunteer_register/', VUserRegistrationView.as_view(), name = 'register'),
    path('organization_register/', OUserRegistrationView.as_view(), name = 'register'),
]