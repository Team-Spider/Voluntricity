from django.contrib import admin
from .models import Vprofile


@admin.register(Vprofile)
class VprofileAdmin(admin.ModelAdmin):
    search_fields = ("username", "first_name")
    
    fieldsets = (
        (
            "Personal Info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "user",
                    "gender",
                    "preferred_pronoun",
                    "date_of_birth",
                    "dietary_preferences",
                    "allergies",
                    "bio",
                    "profile_pic",
                ),
            },
        ),
        (
            "Contact Info",
            {
                "fields": (
                    "phone_number",
                    "facebook_link",
                    "linkedin_link",
                    "instagram_link",
                )
            }
        ),
        (
            "Address Info",
            {
                "fields": (
                    "address_line1",
                    "address_line2",
                    "city",
                    "country",
                    "postal_code",
                ),
            },
        ),
    )

