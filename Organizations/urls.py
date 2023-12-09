from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name = 'signup'),
    path('signin/', views.signin, name = 'signin'),
    path('activate/<uidb64>/<token>',views.activate, name="activate"),
    path('', views.home, name = 'home'),
    path('set_profile', views.set_profile, name = 'set_profile')
]