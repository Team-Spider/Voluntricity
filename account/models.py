from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    is_volunteer = models.BooleanField(default=False)
    is_organization = models.BooleanField(default=False)
    tc = models.BooleanField(default=False)
    name = models.CharField(max_length=300, default=None, null = True)
    password2 = models.CharField(max_length=128)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)

    # Ensure that only one of is_volunteer or is_organization is True
    def clean(self):
        super().clean()
        if self.is_volunteer and self.is_organization:
            raise ValidationError(_("User cannot be both volunteer and organization."))

    # Ensure email field is unique
    def save(self, *args, **kwargs):
        self.email = self.email.lower()  # Ensure email is saved in lowercase
        if not self.pk:  # New user
            if CustomUser.objects.filter(email=self.email).exists():
                raise ValidationError(_("Email must be unique."))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email
    
class VolunteerUser(CustomUser):
    class Meta:
        proxy = True

class OrganizationUser(CustomUser):
    class Meta:
        proxy = True
