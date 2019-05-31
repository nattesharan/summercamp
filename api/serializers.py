from rest_framework import serializers
from django.contrib.auth.models import Group, User
from api.models import ActivityCategories
from rest_framework.validators import UniqueValidator

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('name','id',)
    
class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityCategories
        fields = ('name','id',)

class UserSignUpSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    username = serializers.CharField(validators=[UniqueValidator(queryset=User.objects.all())])
    password1= serializers.CharField()
    password2= serializers.CharField()
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])
    description = serializers.CharField(required=False)
    city=serializers.CharField(required=False)
    age=serializers.IntegerField()
    phone = serializers.CharField(min_length=10, max_length=10)
    gender = serializers.ChoiceField(choices=['M','F'])
    image = serializers.ImageField(required=False)
    role = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all(), write_only=True)

    def validate(self, attrs):
        if not attrs.get('password1') == attrs.get('password2'):
            raise serializers.ValidationError("Passwords do not match.")
        return attrs
    
    def create(self, validated_data):
        try:
            user = User.objects.create_user(username=validated_data['username'],email=validated_data['email'],
                                            password=validated_data['password1'],first_name=validated_data['first_name'],
                                            last_name=validated_data['last_name'])
            profile = user.profile
            profile.update_profile(description=validated_data.get('description',None), city=validated_data.get('city', None),
                                    age=validated_data.get('age'), phone=validated_data.get('phone'), gender=validated_data.get('gender'),
                                    image=validated_data.get('image',None))
            user.groups.add(validated_data['role'])
            return True, "Successfully registered the user"
        except Exception as E:
            return False, str(E)

