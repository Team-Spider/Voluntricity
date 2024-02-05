from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    # Define fields displayed in the user list view
    list_display = ('username', 'email', 'is_active', 'is_staff', 'is_superuser', 'is_volunteer', 'is_organization')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'is_volunteer', 'is_organization')
    search_fields = ('username', 'email')
    ordering = ('-date_joined',)  # Sort by latest joined by default

    # Fieldsets for editing user details
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_volunteer', 'is_organization')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    # Add fields for adding a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser', 'is_volunteer', 'is_organization')}
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

admin.site.register(CustomUser, CustomUserAdmin)
