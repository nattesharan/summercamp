from django.test import Client
import pytest

@pytest.mark.django_db
class TestCategoriesAndGroups:
    client = Client()
    base_ep = '/api/v1/'
    categories_ep = '{}{}'.format(base_ep, 'categories/')
    groups_ep = '{}{}'.format(base_ep, 'groups/')

    def test_categories(self, categories):
        response = self.client.get(self.categories_ep)
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 5
    
    def test_groups(self, groups):
        response = self.client.get(self.groups_ep)
        data = response.json()
        assert response.status_code == 200
        assert len(data) == 3