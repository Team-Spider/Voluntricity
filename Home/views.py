from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import get_user_model

# Create your views here.
def home(request):
    if request.user.is_authenticated:
        user = request.user
        if user.is_volunteer:
            return redirect('volunteers/')
        if user.is_organization:
            return redirect('organizations/')
    return render(request, 'index.html')

def signup(request):
    return render(request, 'signup.html')

def signin(request):
    return render(request, 'signin.html')