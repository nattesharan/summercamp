from rest_framework import serializers
from django.contrib.auth.models import Group, User
from django.contrib.auth import authenticate
from api.models import ActivityCategories, SummerCamp, SummerCampActivities
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

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(username=data.get('username'), password=data.get('password'))
        if user:
            if user.is_active:
                data['user'] = user
                return data
            raise serializers.ValidationError('User not active.')
        raise serializers.ValidationError('Invalid credentials.')

class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = SummerCampActivities
        fields = '__all__'
        read_only_fields = ('summer_camp', 'participants')

class SummercampSerializer(serializers.ModelSerializer):
    camp_activities = ActivitySerializer(many=True, required=False)
    class Meta:
        model = SummerCamp
        fields = (
            'id',
            'name',
            'description',
            'slug',
            'is_active',
            'start_date',
            'end_date',
            'created',
            'owner',
            'camp_activities'
        )
        read_only_fields = ('owner',)

class UserSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField(method_name='get_image_url')
    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'email',
            'image'
        )
    
    def get_image_url(self, instance):
        request = self.context.get('request')
        return request.build_absolute_uri(instance.profile.image.url)