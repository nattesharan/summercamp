import pytest
from django.contrib.auth.models import Group

@pytest.fixture
def groups(request):
    group_names = ['student', 'instructor', 'organiser']
    for group_name in group_names:
        group, status = Group.objects.get_or_create(name=group_name)