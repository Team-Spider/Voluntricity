from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('signup/', views.signup, name = 'signUp'),
    path('signin/', views.signin, name='signin'),
    path('events/',views.events, name='events'),
]