from django.db import models
from django.utils.translation import gettext as _
from Home.models import CustomUser

class Oprofile(models.Model):
    # Organization Information
    organization_name = models.CharField(_('Organization Name'), max_length=255)
    description = models.TextField(_('Description'), blank=True)
    website = models.URLField(_('Website'), blank=True)

    # Address Information
    address_line1 = models.CharField(_('Address Line 1'), max_length=255)
    address_line2 = models.CharField(_('Address Line 2'), max_length=255, blank=True)
    city = models.CharField(_('City'), max_length=100)
    country = models.CharField(_('Country'), max_length=100)
    postal_code = models.CharField(_('Postal Code'), max_length=10)

    # Contact Information
    phone_number = models.CharField(_('Phone Number'), max_length=15, blank=True)

    # Social Links
    facebook_link = models.URLField(_('Facebook Link'), blank=True)
    linkedin_link = models.URLField(_('LinkedIn Link'), blank=True)
    instagram_link = models.URLField(_('Instagram Link'), blank=True)

    # Logo (Profile Picture)
    logo = models.ImageField(
        _('Logo'),
        upload_to='organization_logos/', 
        blank=True,
        null=True,
    )

    # Link the organization profile to a user (assuming you have a User model)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)  # Replace 'YourUserModel' with your actual User model

    def __str__(self):
        return self.organization_name

class Event(models.Model):
    event_name = models.CharField(max_length=255)
    event_description = models.TextField()
    event_date = models.DateField()
    event_location = models.CharField(max_length=255)
    event_time = models.TimeField()
    registration_deadline = models.DateField()
    registered = models.IntegerField(default=0)
    total_volunteers_required = models.IntegerField()
    banner = models.ImageField(
        _('Logo'),
        upload_to='event_banners/', 
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.event_name

class Requirement(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    requirement_name = models.CharField(max_length=255, primary_key=True)
    requirement_description = models.TextField()

    def __str__(self):
        return self.requirement_name

class IncludedItem(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    included_name = models.CharField(max_length=255, primary_key=True)
    included_description = models.TextField()

    def __str__(self):
        return self.included_name

