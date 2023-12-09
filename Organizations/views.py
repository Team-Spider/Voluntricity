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
from .models import Oprofile
from Voluntricity import settings 
import hashlib, secrets

def generate_unique_code(organization_name):
    max_username_length = 16  # Set the maximum allowed length for the username

    while True:
        # Generate a random salt
        salt = secrets.token_hex(8)  # Use a shorter salt for shorter usernames

        # Combine the organization name and salt
        data = organization_name + salt

        # Calculate the SHA-256 hash
        unique_code = hashlib.sha256(data.encode()).hexdigest()

        # Trim the unique code to fit within the maximum username length
        unique_username = (
            f"ORG_{unique_code[:max_username_length-4]}"  # Subtract 4 for 'ORG_' prefix
        )

        # Check if the username is already registered
        if not CustomUser.objects.filter(username=unique_username).exists():
            return unique_username

# Create your views here.
def home(request):
    return render(request, 'otemplates/index.html')

def signup(request):
    if request.method == "POST":
        name = request.POST["fname"]
        email = request.POST["email"]
        pass1 = request.POST["pass1"]
        pass2 = request.POST["pass2"]
        username = generate_unique_code(name)

        # Check if the username or email is already taken
        if CustomUser.objects.filter(username=username).exists() or CustomUser.objects.filter(email=email).exists():
            return render(request, 'otemplates/signup.html', {'emessage': 'Username or email already exists'})
        
        # Check if passwords match
        if pass1 != pass2:
            return render(request, 'otemplates/signup.html', {'emessage': 'Passwords do not match'})
        
        try:
            password_validation.validate_password(pass1)

        except ValidationError as e:
            return render(request, "otemplates/signup.html", {"pmessage": e.messages})


        # Create a new user
        user = CustomUser.objects.create_user(email=email, password=pass1, username=username)
        user.is_organization = True
        user.is_active = False
        user.save()
        
        profile = Oprofile(user = user)
        profile.organization_name = name
        profile.save()
        
        # Email address confirmation email
        current_site = get_current_site(request)
        email_subject = "COnfirm your email for Voluntricity"
        message2 = render_to_string(
            "otemplates/email_confirmation.html",
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
        
        
    return render(request, 'otemplates/signup.html')

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
        return redirect("/organizations/signin")

    else:
        messages.error(request, "Invalid Email")
        return redirect("/organizations/signup")
    
def signin(request):
    if request.method == "POST":
        email = request.POST["email"]
        pass1 = request.POST["pass1"]

        # Authenticate and login the user
        authenticated_user = authenticate(request, email = email, password=pass1)
        if authenticated_user is not None:
            login(request, authenticated_user)

            # Redirect to a success page or home page
            return redirect('/organizations')
        
        else:
            messages.error(request, "Bad Credentials!")
            return redirect("/organizations/signin")

    return render(request, "otemplates/signin.html")

@login_required
def set_profile(request):
    user = request.user
    profile = Oprofile.objects.get(user=user)
    context = {
        "orgname": profile.organization_name,
        "description": profile.description,
        "email": user.email,
        "instagram": profile.instagram_link,
        "facebook": profile.facebook_link,
        "linkedin": profile.linkedin_link,
        "website": profile.website, 
        "pic": profile.logo.url if profile.logo else None,
        "line1": profile.address_line1,
        "line2": profile.address_line2,
        "city": profile.city,
        "postal": profile.postal_code,
        "country": profile.country,
        "contact": profile.phone_number,
    }
    return render(request, "otemplates/profile.html", context)

@login_required
def social_links(request):
    if request.method == "POST":
        instagram = request.POST['instagram']
        facebook = request.POST['facebook']
        linkedin = request.POST['linkedin']
        
        user = request.user
        profile = Oprofile.objects.get(user = user)
        profile.instagram_link = instagram
        profile.facebook_link = facebook
        profile.linkedin_link = linkedin
        profile.save()
        return redirect('/organizations/set_profile')
    
    return redirect('/organizations/set_profile')

@login_required
def personal_info(request):
    if request.method == "POST":
        
        orgname = request.POST['organization-name']
        website = request.POST['website']
        description = request.POST['description']
        logo = request.FILES.get('logo')
        
        user = request.user
        profile = Oprofile.objects.get(user = user)
        profile.organization_name = orgname
        profile.website = website
        profile.description = description
        profile.logo = logo
        profile.save()
        
        return redirect('/organizations/set_profile')
    
    return redirect('/organizations/set_profile')

@login_required
def address_info(request):
    if request.method=="POST":
        line1=request.POST['address1']
        line2=request.POST['address2']
        city=request.POST['City']
        postal=request.POST['Postal']
        country=request.POST['Country']        

        user=request.user
        profile=Oprofile.objects.get(user=user)
        profile.address_line1=line1
        profile.address_line2=line2
        profile.city=city
        profile.postal_code=postal
        profile.country=country
        profile.save()
        
        return redirect('/organizations/set_profile')

    return redirect('/organizations/set_profile')

@login_required
def contact_info(request):
    if request.method=="POST":
        contact=request.POST['contact']

        user=request.user
        profile=Oprofile.objects.get(user=user)
        profile.phone_number=contact
        profile.save()

        return redirect('/organizations/set_profile')

    return redirect('/organizations/set_profile')