from rest_framework import viewsets
from django.contrib.auth.models import Group, User
from api.serializers import (GroupSerializer, CategoriesSerializer, UserSignUpSerializer,
                            LoginSerializer, SummercampSerializer, UserSerializer)
from api.models import ActivityCategories, SummerCamp
from rest_framework import generics, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import login
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from api.permissions import IsOrganiser
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
    
    def get_queryset(self):
        return self.request.user.summer_camps.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class InstructorsView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['get',]
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsOrganiser)

    def get_queryset(self):
        group = Group.objects.get(name='instructor')
        return group.user_set.all()