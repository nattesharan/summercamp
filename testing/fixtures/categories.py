import pytest
from api.models import ActivityCategories

@pytest.fixture
def categories(request):
    category_names = ['swimming', 'hiking', 'cricket', 'music', 'tennis']
    for category_name in category_names:
        category, status = ActivityCategories.get_or_create(category_name)
