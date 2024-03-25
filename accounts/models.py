from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class Profile(models.Model):
    User = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.IntegerField(null=True, blank=True)
    address = models.CharField(max_length=300, null=True, blank=True)
    profile_image = models.ImageField(upload_to='profile/',  null=True, blank=True)
    #you can to use from default in profile_image

    def __str__(self):
        return self.User.username

def Save_Profile_User(sender, **kwargs):
    if kwargs['created']:
        profile_user = Profile(User=kwargs['instance'])
        profile_user.save()

post_save.connect(Save_Profile_User, sender=User)