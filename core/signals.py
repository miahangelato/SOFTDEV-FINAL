from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from .models import Profile
User = get_user_model()
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


#This code defines a signal handler function named create_profile that automatically creates a Profile object associated with a newly created user instance when the user is created.

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()