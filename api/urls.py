from rest_framework import routers
from django.conf.urls import url
from api.views import UserGroupsView, CategoriesView

router = routers.DefaultRouter()

router.register(r'^groups', UserGroupsView)

urlpatterns = router.urls

urlpatterns += [
    url(r'^categories/$', CategoriesView.as_view(), name='api_categories')
]