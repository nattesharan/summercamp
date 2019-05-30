from rest_framework import serializers
from django.contrib.auth.models import Group
from api.models import ActivityCategories

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('name','id',)
    
class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityCategories
        fields = ('name','id',)