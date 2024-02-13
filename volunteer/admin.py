from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *


class VolunteerUserAdmin(UserAdmin):
    # Define fields displayed in the user list view
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser', 'tc')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'email')
    ordering = ('-date_joined',)  # Sort by latest joined by default

    # Fieldsets for editing user details
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password', 'first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'tc')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    # Add fields for adding a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser', 'tc')}
        ),
    )

    def get_queryset(self, request):
        # Filter queryset to only include volunteer users
        return super().get_queryset(request).filter(is_volunteer=True)

    # Customize user search functionality
    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        try:
            search_term_as_int = int(search_term)
            queryset |= self.model.objects.filter(last_login=search_term_as_int)
        except ValueError:
            pass  # Search term is not an integer
        return queryset, use_distinct

    def save_model(self, request, obj, form, change):
        """
        Given a model instance save it to the database.
        """
        if not obj.pk:  # If it's a new object
            obj.is_volunteer = True  # Set is_volunteer to True
        super().save_model(request, obj, form, change)


class VprofileAdmin(admin.ModelAdmin):
    list_display = ('user', 'gender', 'date_of_birth', 'city', 'country', 'get_profile_pic_filename')
    search_fields = ('user__username', 'city', 'country')

    fieldsets = (
        ('Personal Information', {
            'fields' : ('user', 'gender', 'preferred_pronoun', 'bio', 'date_of_birth')}),
        ('Address Information', { 'fields' : ('address_line1', 'address_line2', 'city', 'country', 'postal_code')}), 
        ('Additional Information', { 'fields' : ('dietary_preferences', 'allergies')}),
        ('Social Links', { 'fields' : ('instagram_link', 'facebook_link', 'linkedin_link')}),
        ('Profile Picture', { 'fields' : ('profile_pic',)}),
        )
    
    def get_queryset(self, request):
        # Filter queryset to only include volunteer users
        return super().get_queryset(request).filter(user__is_volunteer=True)

    def get_profile_pic_filename(self, obj):
        if obj.profile_pic:
            return obj.profile_pic.name.split('/')[-1]
        return 'No profile picture'
    get_profile_pic_filename.short_description = 'Profile Picture Filename'


class SkillsAdmin(admin.ModelAdmin):
    list_display = ('id', 'skill', 'Category')
    search_fields = ('id', 'skill', 'Category')


admin.site.register(Vprofile, VprofileAdmin)
admin.site.register(Skills, SkillsAdmin)
admin.site.register(VolunteerUser, VolunteerUserAdmin)
