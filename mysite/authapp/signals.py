from .models import ShopUser, ShopUserProfile

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


@receiver(post_save, sender=ShopUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        ShopUserProfile.objects.create(user=instance)


@receiver(post_save, sender=ShopUser)
def update_user_profile(sender, instance, **kwargs):
    instance.shopuserprofile.save()
