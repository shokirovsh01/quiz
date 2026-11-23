from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    pass

class Role(models.Model):
    role_name = models.CharField(max_length=123, unique=True)

    def __str__(self):
        return self.role_name

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    fullname = models.CharField(max_length=123, blank=True)
    bio = models.TextField(blank=True)
    role = models.ForeignKey(Role,on_delete=models.CASCADE)
    task_count = models.PositiveIntegerField(default=0)
    phone = models.CharField(max_length=20, blank=True)
    avatar = models.CharField(max_length=123, blank=True)

    def __str__(self):
        return  self.user.username


@receiver(post_save, sender=CustomUser)
def create_profile(sender, instance, created, **kwargs):
    if created:
        role, _ = Role.objects.get_or_create(role_name='student')
        Profile.objects.get_or_create(user=instance, defaults={'role': role})
