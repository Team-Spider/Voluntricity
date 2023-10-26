from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name = 'signup'),
    path('signin/', views.signin, name = 'signin'),
    path('activate/<uidb64>/<token>',views.activate, name="activate"),
    path('', views.home, name = 'lol'),
    path('set_profile/', views.set_profile, name = "profile_form"),
    path('social_links', views.social_links, name = 'social_links'),
    path('personal_info', views.personal_info, name = 'personal_info'),
]