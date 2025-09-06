from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import UserProfile, Organization

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile_for_user(sender, instance, created, **kwargs):
    if created:
        # Si aún no existe una organización, creamos una por defecto “Personal”
        org, _ = Organization.objects.get_or_create(name=f"Org - {instance.username}")
        UserProfile.objects.create(user=instance, organization=org)
