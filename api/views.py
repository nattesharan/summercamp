from rest_framework import viewsets
from django.contrib.auth.models import Group
from api.serializers import GroupSerializer, CategoriesSerializer
from api.models import ActivityCategories
from rest_framework import generics, mixins
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
    