from django.shortcuts import render, HttpResponse, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import login, authenticate, password_validation
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from Voluntricity.tokens import generate_token
from django.utils.encoding import force_bytes
from django.contrib import messages
from django.core.mail import EmailMessage
from Home.models import CustomUser
from .models import Vprofile
from Voluntricity import settings
import re

def convert_date_format(date_of_birth):
    formatted_date = date_of_birth.strftime("%Y-%m-%d")
    return formatted_date

def isnot_valid_userstring(input_string):
    # Define the regular expression pattern for the given conditions
    pattern = r"^[A-Za-z0-9@/./+/-/_]{1,150}$"

    # Use re.match to check if the input string matches the pattern
    if re.match(pattern, input_string):
        return False
    else:
        return True

# Create your views here.
@login_required
def home(request):
    return render(request, 'vtemplates/index.html')

def signup(request):
    if request.method == "POST":
        username = request.POST["username"]
        fname = request.POST["fname"]
        lname = request.POST["lname"]
        email = request.POST["email"]
        pass1 = request.POST["pass1"]
        pass2 = request.POST["pass2"]

        # Check if the username or email is already taken
        if CustomUser.objects.filter(username=username).exists() or CustomUser.objects.filter(email=email).exists():
            return render(request, 'vtemplates/signup.html', {'emessage': 'Username or email already exists'})
        
        # Check if passwords match
        if pass1 != pass2:
            return render(request, 'vtemplates/signup.html', {'emessage': 'Passwords do not match'})
        
        try:
            password_validation.validate_password(pass1)

        except ValidationError as e:
            return render(request, "vtemplates/signup.html", {"pmessage": e.messages})
        
        if isnot_valid_userstring(username):
            return render(request, 'vtemplates/signup.html', {'emessage': 'Not a valid Username'})

        # Create a new user
        user = CustomUser.objects.create_user(email=email, password=pass1, username=username)
        user.is_volunteer = True
        user.is_active = False
        user.save()
        
        profile = Vprofile(user = user)
        profile.first_name = fname
        profile.last_name = lname
        profile.save()
        
        # Email address confirmation email
        current_site = get_current_site(request)
        email_subject = "Confirm your email for Voluntricity"
        message2 = render_to_string(
            "vtemplates/email_confirmation.html",
            {
                "name": user.username,
                "domain": current_site.domain,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": generate_token.make_token(user),
            },
        )
        email = EmailMessage(
            email_subject,
            message2,
            settings.EMAIL_HOST_USER,
            [user.email],
        )
        email.fail_silently = True
        email.send()

        return render(request, 'message.html')
        
        
    return render(request, 'vtemplates/signup.html')

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        myuser = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active = True
        myuser.save()
        messages.success(request, "Account Activated")
        return redirect("/volunteers/signin")

    else:
        messages.error(request, "Invalid Email")
        return redirect("/volunteers/signup")
    
def signin(request):
    if request.method == "POST":
        email = request.POST["email"]
        pass1 = request.POST["pass1"]

        # Authenticate and login the user
        authenticated_user = authenticate(request, email = email, password=pass1)
        if authenticated_user is not None:
            login(request, authenticated_user)

            # Redirect to a success page or home page
            return redirect('/volunteers')
        
        else:
            messages.error(request, "Bad Credentials!")
            return redirect("/volunteers/signin")

    return render(request, "vtemplates/signin.html")

@login_required
def set_profile(request):
    user = request.user
    profile = Vprofile.objects.get(user=user)
    context = {
        "username": user.username,
        "email": user.email,
        "instagram": profile.instagram_link,
        "facebook": profile.facebook_link,
        "linkedin": profile.linkedin_link,
        "fname": profile.first_name,
        "lname": profile.last_name,
        "dob": convert_date_format(profile.date_of_birth),
        "Gender": profile.gender,
        "pn": profile.preferred_pronoun,
        "dp": profile.dietary_preferences,
        "allergies": profile.allergies,
        "bio": profile.bio,
        "pic": profile.profile_pic.url if profile.profile_pic else None,
        "line1": profile.address_line1,
        "line2": profile.address_line2,
        "city": profile.city,
        "postal": profile.postal_code,
        "country": profile.country,
        "contact": profile.phone_number,
    }
    return render(request, "vtemplates/profile.html", context)


@login_required
def social_links(request):
    if request.method == "POST":
        instagram = request.POST['instagram']
        facebook = request.POST['facebook']
        linkedin = request.POST['linkedin']
        
        user = request.user
        profile = Vprofile.objects.get(user = user)
        profile.instagram_link = instagram
        profile.facebook_link = facebook
        profile.linkedin_link = linkedin
        profile.save()
        return redirect('/volunteers/set_profile')
    
    return redirect('/volunteers/set_profile')

@login_required
def personal_info(request):
    if request.method == "POST":
        
        fname = request.POST['first-name']
        lname = request.POST['last-name']
        dob = request.POST['DateOfBirth']
        Gender = request.POST['Gender']
        pn = request.POST['PreferredPronoun']
        dp = request.POST['DietaryPreferences']
        allergies = request.POST['Allergies']
        bio = request.POST['bio']
        pic = request.FILES.get('profilePicture')
        
        user = request.user
        profile = Vprofile.objects.get(user = user)
        profile.first_name = fname
        profile.last_name = lname
        profile.date_of_birth = dob
        profile.gender = Gender
        profile.preferred_pronoun = pn
        profile.dietary_preferences = dp
        profile.allergies = allergies
        profile.bio = bio
        profile.profile_pic = pic
        profile.save()
        
        return redirect('/volunteers/set_profile')
    
    return redirect('/volunteers/set_profile')

@login_required
def address_info(request):
    if request.method=="POST":
        line1=request.POST['address1']
        line2=request.POST['address2']
        city=request.POST['City']
        postal=request.POST['Postal']
        country=request.POST['Country']        

        user=request.user
        profile=Vprofile.objects.get(user=user)
        profile.address_line1=line1
        profile.address_line2=line2
        profile.city=city
        profile.postal_code=postal
        profile.country=country
        profile.save()
        
        return redirect('/volunteers/set_profile')

    return redirect('/volunteers/set_profile')

@login_required
def contact_info(request):
    if request.method=="POST":
        contact=request.POST['contact']

        user=request.user
        profile=Vprofile.objects.get(user=user)
        profile.phone_number=contact
        profile.save()

        return redirect('/volunteers/set_profile')

    return redirect('/volunteers/set_profile')

        