from django.contrib import admin
from .models import Oprofile


@admin.register(Oprofile)
class OprofileAdmin(admin.ModelAdmin):
    search_fields = ("username", "email", "organization_name")

    fieldsets = (
        (
            "Personal Info",
            {
                "fields": (
                    "organization_name",
                    "user",
                    "description",
                    "logo",
                ),
            },
        ),
        (
            "Contact Info",
            {
                "fields": (
                    "website",
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
