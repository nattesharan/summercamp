from rest_framework import routers
from django.conf.urls import url
from api.views import (UserGroupsView, CategoriesView, RegisterView, LoginView, 
                        SummercampView, InstructorsView, UserSummerCampView)

router = routers.DefaultRouter()

router.register(r'^groups', UserGroupsView)
router.register(r'^camps', SummercampView)
router.register(r'^instructors', InstructorsView)
router.register(r'^summercamps', UserSummerCampView)
urlpatterns = router.urls

urlpatterns += [
    url(r'^categories/$', CategoriesView.as_view(), name='api_categories'),
    url(r'^signup/$', RegisterView.as_view(), name='register_api'),
    url(r'^login/$', LoginView.as_view(), name='login_api')
]