from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser  # Import your CustomUser model

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_volunteer', 'is_organization', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('is_volunteer', 'is_organization', 'is_active', 'is_staff', 'is_superuser')

    fieldsets = (
        ('Personal Information', {'fields': ('email', 'password', 'username')}),
        ('User Type', {'fields': ('is_volunteer', 'is_organization')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_volunteer', 'is_organization'),
        }),
    )

# Register your CustomUser model with the customized admin
admin.site.register(CustomUser, CustomUserAdmin)
