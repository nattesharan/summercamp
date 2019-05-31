from rest_framework import viewsets
from django.contrib.auth.models import Group, User
from api.serializers import (GroupSerializer, CategoriesSerializer, UserSignUpSerializer,
                            LoginSerializer, SummercampSerializer, UserSerializer, ActivitySerializer)
from api.models import ActivityCategories, SummerCamp, SummerCampActivities
from rest_framework import generics, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import login
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from api.permissions import IsOrganiser, IsStudent
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import detail_route

# Create your views here.
class UserGroupsView(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    http_method_names = ['get']

class CategoriesView(generics.GenericAPIView, mixins.ListModelMixin):
    queryset = ActivityCategories.objects.all()
    serializer_class = CategoriesSerializer

    def get(self, request):
        return self.list(request)
    
class RegisterView(APIView):
    def post(self, request):
        data = UserSignUpSerializer(data=request.data)
        data.is_valid(raise_exception=True)
        success, message = data.save()
        if success:
            return Response({'success': success, 'message': message})
        return Response({'success': success, 'message': message}, status=400)

class LoginView(APIView):
    def post(self, request):
        data = LoginSerializer(data=request.data)
        data.is_valid(raise_exception=True)
        user = data.validated_data['user']
        login(request, user)
        token, created= Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user_id': user.pk, 'email': user.email, 'username': user.username})

class SummercampView(viewsets.ModelViewSet):
    queryset = SummerCamp.objects.all()
    serializer_class = SummercampSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsOrganiser)
    lookup_field = 'slug'
    
    def get_queryset(self):
        return self.request.user.summer_camps.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    
    @detail_route(methods=['post'])
    def activities(self, request, slug):
        summer_camp = self.get_object()
        data = ActivitySerializer(data=request.data)
        data.is_valid(raise_exception=True)
        data.save(summer_camp=summer_camp)
        return Response(data.data)

class InstructorsView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['get',]
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsOrganiser)

    def get_queryset(self):
        assigned_instructors = list(SummerCampActivities.objects.filter(is_active=True).values_list('instructor', flat=True))
        group = Group.objects.get(name='instructor')
        return group.user_set.exclude(pk__in=assigned_instructors)


class UserSummerCampView(viewsets.ModelViewSet):
    queryset = SummerCamp.objects.all()
    serializer_class = SummercampSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsStudent)
    http_method_names = ['get', 'post']

    @detail_route(methods=['post'])
    def join(self, request, pk):
        summer_camp = self.get_object()
        if 'activities' not in request.data or not request.data['activities']:
            return Response({'status': False, 'message': 'Please select activities to participate.'}, status=400)
        for activity_id in request.data['activities']:
            try:
                summer_camp_activity = summer_camp.camp_activities.get(pk=activity_id)
                summer_camp_activity.participants.add(request.user)
            except ObjectDoesNotExist:
                return Response({'status': False, 'message': 'Invalid activity selected.'}, status=400)
        return Response({'status': True, 'message': 'Successfully added user to summercamp'})

class DashboardView(viewsets.ModelViewSet):
    serializer_class = ActivitySerializer
    queryset = SummerCampActivities.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get']

    def get_serializer_class(self):
        user = self.request.user
        role = user.groups.first().name
        if role in ['student','instructor']:
            return self.serializer_class
        return SummercampSerializer

    def get_queryset(self):
        user = self.request.user
        role = user.groups.first().name
        if role == 'student':
            return user.my_activities.all()
        elif role == 'organiser':
            return user.summer_camps.all()
        else:
            return user.activities.all()
