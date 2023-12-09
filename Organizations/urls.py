from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name = 'signup'),
    path('signin/', views.signin, name = 'signin'),
    path('activate/<uidb64>/<token>',views.activate, name="activate"),
    path('', views.home, name = 'home'),
    path('set_profile', views.set_profile, name = 'set_profile'),
    path('social_links', views.social_links, name = "social_links"),
    path('personal_info', views.personal_info, name = "personal_info"),
    path('address_info', views.address_info, name= "address_info"),
    path('contact_info', views.contact_info, name="contact_info")
]