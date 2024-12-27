from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.apps import apps
import random


def random_number():
    return str(random.randint(0, 256))

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_color = models.CharField(max_length=100,
        default='('+str(random.randint(0, 256))+','+str(random.randint(0, 256))+','+str(random.randint(0, 256))+','+'.3'+')')
    def __str__(self):
        return "@{}".format(self.user.username)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
