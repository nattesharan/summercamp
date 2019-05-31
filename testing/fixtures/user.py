import pytest
from django.contrib.auth.models import Group, User

@pytest.fixture
def instructor_user(request, groups):
    user = User.objects.create_user(username="testuser1",email="testuser1@gmail.com",password="testuser1",
                                    first_name="test",last_name="user1")
    profile = user.profile
    profile.update_profile(description="user for testing", city="testcity1",age=24, phone="1234567890", gender="M")
    group = Group.objects.get(name='instructor')
    user.groups.add(group)
    return user
