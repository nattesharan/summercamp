# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2019-05-30 08:22
from __future__ import unicode_literals

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(default='', max_length=256)),
                ('city', models.CharField(default='', max_length=32)),
                ('age', models.IntegerField(default=23)),
                ('phone', models.CharField(max_length=10, validators=[django.core.validators.MinLengthValidator(10)])),
                ('image', models.ImageField(blank=True, upload_to='profile_images')),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=1)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
