# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2019-05-31 09:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_activitycategories'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='image',
            field=models.ImageField(blank=True, default='https://cdn.pixabay.com/photo/2016/08/08/09/17/avatar-1577909_960_720.png', upload_to='profile_images'),
        ),
    ]