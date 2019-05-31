from rest_framework import viewsets
from django.contrib.auth.models import Group
from api.serializers import GroupSerializer, CategoriesSerializer, UserSignUpSerializer, LoginSerializer
from api.models import ActivityCategories
from rest_framework import generics, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import login

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