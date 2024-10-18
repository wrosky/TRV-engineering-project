from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, FriendList

@receiver(post_save, sender=User)
def create_friendlist(sender, instance, created, **kwargs):
    if created:
        FriendList.objects.create(user=instance)