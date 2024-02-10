from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

class CustomUserAdmin(UserAdmin):
    # Define fields displayed in the user list view
    list_display = ('username', 'email', 'is_active', 'is_staff', 'is_superuser', 'is_volunteer', 'is_organization', 'tc')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'is_volunteer', 'is_organization')
    search_fields = ('username', 'email')
    ordering = ('-date_joined',)  # Sort by latest joined by default

    # Fieldsets for editing user details
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_volunteer', 'is_organization', 'tc')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    # Add fields for adding a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser', 'is_volunteer', 'is_organization', 'tc')}
        ),
    )

    # Customize user search functionality
    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        try:
            search_term_as_int = int(search_term)
            queryset |= self.model.objects.filter(last_login=search_term_as_int)
        except ValueError:
            pass  # Search term is not an integer
        return queryset, use_distinct


class OrganizationUserAdmin(UserAdmin):
    # Define fields displayed in the user list view
    list_display = ('name', 'email', 'is_active', 'is_staff', 'is_superuser', 'tc')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'email')
    ordering = ('-date_joined',)  # Sort by latest joined by default

    # Fieldsets for editing user details
    fieldsets = (
        (None, {'fields': ('name', 'email', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'tc')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    # Add fields for adding a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'email', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser', 'tc')}
        ),
    )

    def get_queryset(self, request):
        # Filter queryset to only include volunteer users
        return super().get_queryset(request).filter(is_organization=True)

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
            obj.is_organization = True  # Set is_volunteer to True
            username = obj.name.lower().replace(' ', '_')
        
            # Check if username already exists, if so, add a number suffix
            suffix = 1
            while CustomUser.objects.filter(username=username).exists():
                username = f"{obj.namename.lower().replace(' ', '_')}{suffix}"
                suffix += 1
            obj.username = username
            
        super().save_model(request, obj, form, change)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(OrganizationUser, OrganizationUserAdmin)
