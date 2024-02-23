import os
from django.db import models
from account.models import CustomUser
from django.utils.translation import gettext_lazy as _
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save


class VolunteerUser(CustomUser):
    class Meta:
        proxy = True

GENDER_CHOICES = [
    ('M', _('Male')),
    ('F', _('Female')),
    ('O', _('Other')),
]

PREFERED_PRONOUN_CHOICES = [
    ('He', _('He/Him')),
    ('She', _('She/Her')),
    ('They', _('They/Them')),
]

class Vprofile(models.Model):
    # Personal Information
    gender = models.CharField(_('Gender'), max_length=1, choices=GENDER_CHOICES)
    preferred_pronoun = models.CharField(_('Preferred Pronoun'), max_length=4, choices=PREFERED_PRONOUN_CHOICES)
    bio = models.TextField(_('Bio'), blank=True)
    
    # Date of Birth
    date_of_birth = models.DateField(_('Date of Birth'), blank=True, null=True)

    # Address Information
    address_line1 = models.CharField(_('Address Line 1'), max_length=255)
    address_line2 = models.CharField(_('Address Line 2'), max_length=255, blank=True)
    city = models.CharField(_('City'), max_length=100)
    country = models.CharField(_('Country'), max_length=100)
    postal_code = models.CharField(_('Postal Code'), max_length=10)

    # Additional Information
    dietary_preferences = models.TextField(_('Dietary Preferences'), blank=True)
    allergies = models.TextField(_('Allergies'), blank=True)
    
    # Social Links
    instagram_link = models.URLField(_('Instagram Link'), blank=True)
    facebook_link = models.URLField(_('Facebook Link'), blank=True)
    linkedin_link = models.URLField(_('LinkedIn Link'), blank=True)

    # Profile Picture
    profile_pic = models.ImageField(
        _('Profile Picture'),
        upload_to='media/profile_pics/',  # Save uploaded files in 'profile_pics/' directory
        blank=True,
        null=True,
    )

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)  

    def __str__(self):
        return str(self.user)
    
# Signal to delete the old profile picture before saving the new one
@receiver(pre_save, sender=Vprofile)
def delete_previous_profile_pic(sender, instance, **kwargs):
    try:
        old_instance = Vprofile.objects.get(pk=instance.pk)
        if old_instance.profile_pic and instance.profile_pic != old_instance.profile_pic:
            # Delete the old profile picture file
            if os.path.isfile(old_instance.profile_pic.path):
                os.remove(old_instance.profile_pic.path)
    except Vprofile.DoesNotExist:
        pass

# Signal to create a Vprofile instance whenever a new VolunteerUser is created
@receiver(post_save, sender=VolunteerUser)
def create_vprofile(sender, instance, created, **kwargs):
    if created:
        Vprofile.objects.create(user=instance)

# Signal to save the Vprofile instance whenever the VolunteerUser is saved
@receiver(post_save, sender=VolunteerUser)
def save_vprofile(sender, instance, **kwargs):
    instance.vprofile.save()


class VolunteerSkills(models.Model):
    skill = models.ForeignKey('Skills', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.skill
    

class Skills(models.Model):
    skill = models.CharField(_('Skill'), max_length=100)
    Category = models.CharField(_('Category'), max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    last_modefied = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.skill