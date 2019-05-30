from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from django.core.exceptions import ObjectDoesNotExist
# Create your models here.

class UserProfile(models.Model):
    GENDER = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    user = models.OneToOneField(User, related_name='profile')
    description = models.CharField(max_length=256, default='')
    city = models.CharField(max_length = 32,default='')
    age = models.IntegerField(default=23)
    phone = models.CharField(max_length=10, validators=[MinLengthValidator(10)])
    image = models.ImageField(upload_to='profile_images', blank=True)
    gender = models.CharField(max_length=1, choices=GENDER)

    def __str__(self):
        return self.user.username

def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = UserProfile.objects.create(user=kwargs['instance'])

post_save.connect(create_profile, sender=User)

class ActivityCategories(models.Model):
    name = models.CharField(max_length=100, blank=False)

    @classmethod
    def get_or_create(cls, category_name):
        try:
            category = cls.objects.get(name=category_name)
            return category, False
        except ObjectDoesNotExist:
            category = cls.objects.create(name=category_name)
            return category, True
