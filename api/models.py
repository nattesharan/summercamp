from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from django.core.exceptions import ObjectDoesNotExist
from django.utils.text import slugify
# Create your models here.

class UserProfile(models.Model):
    GENDER = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    description = models.CharField(max_length=256, default='')
    city = models.CharField(max_length = 32,default='')
    age = models.IntegerField(default=23)
    phone = models.CharField(max_length=10, validators=[MinLengthValidator(10)])
    image = models.ImageField(upload_to='profile_images', blank=True, default='https://cdn.pixabay.com/photo/2016/08/08/09/17/avatar-1577909_960_720.png')
    gender = models.CharField(max_length=1, choices=GENDER)

    def __str__(self):
        return self.user.username
    
    def update_profile(self, **kwargs):
        for key, value in kwargs.items():
            if value:
                setattr(self, key, value)
        self.save()
        return True

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

class SummerCamp(models.Model):
    name = models.CharField(max_length=64, unique=True)
    description = models.CharField(max_length=256)
    slug = models.SlugField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='summer_camps')
    start_date = models.DateField()
    end_date = models.DateField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

class SummerCampActivities(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    slug = models.SlugField(null=True, blank=True)
    summer_camp = models.ForeignKey(SummerCamp, on_delete=models.CASCADE, related_name='camp_activities')
    category = models.ForeignKey(ActivityCategories, related_name='activities')
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    instructor = models.ForeignKey(User, related_name='activities')
    start_time = models.TimeField()
    end_time = models.TimeField()
    participants = models.ManyToManyField(User, related_name='my_activities')

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        name = self.name + '-' + self.summer_camp.name
        self.slug = slugify(name, allow_unicode=True)
        super().save(*args, **kwargs)
