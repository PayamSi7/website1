from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from phone_field import PhoneField

class Profile(models.Model):
    User = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.IntegerField(null=True, blank=True)
    address = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return self.User.username

def Save_Profile_User(sender, **kwargs):
    if kwargs['created']:
        profile_user = Profile(User=kwargs['instance'])
        profile_user.save()

post_save.connect(Save_Profile_User, sender=User)