from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Vprofile, GENDER_CHOICES

@admin.register(Vprofile)
class VprofileAdmin(admin.ModelAdmin):
    search_fields = ("user__username", "first_name", "last_name")
    
    list_display = ("user", "first_name", "last_name", "gender", "date_of_birth", "phone_number", "city", "country")
    list_filter = ("gender", "country")

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

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        queryset |= self.model.objects.filter(user__email__icontains=search_term)
        return queryset, use_distinct

    def user_info(self, obj):
        return f"{obj.user.username} - {obj.user.email}"
    user_info.short_description = 'User Information'

    def get_list_display_links(self, request, list_display):
        # Make the first column (user_info) a link to the change page
        return ['user']

admin.site.site_header = "Voluntricity Administration"
admin.site.site_title = "Voluntricity Admin Portal"
admin.site.index_title = "Welcome to Voluntricity Admin"


