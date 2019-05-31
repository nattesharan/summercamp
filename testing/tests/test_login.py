from django.test import Client
from django.contrib.auth.models import User
import pytest
import json

@pytest.mark.django_db
class TestUserRegistration:
    client = Client()
    base_ep = '/api/v1/'
    login_ep = "{}{}".format(base_ep, 'login/')

    def test_login_with_username(self, instructor_user):
        headers = {'Content-type': 'application/json'}
        data = {
            'username': 'testuser1',
            'password': 'testuser1'
        }
        response = self.client.post(self.login_ep, data=data, headers = headers)
        assert response.status_code == 200
        assert 'token' in response.json()
    
    def test_login_missing_cred(self, instructor_user):
        headers = {'Content-type': 'application/json'}
        data = {}
        response = self.client.post(self.login_ep, data=data, headers = headers)
        assert response.status_code == 400
    
    def test_login_invalid_pass(self, instructor_user):
        headers = {'Content-type': 'application/json'}
        data = {
            'username': 'testuser1',
            'password': 'testuser11321'
        }
        response = self.client.post(self.login_ep, data=data, headers = headers)
        assert response.status_code == 400
    
    def test_login_with_email(self, instructor_user):
        headers = {'Content-type': 'application/json'}
        data = {
            'username': 'testuser1@gmail.com',
            'password': 'testuser1'
        }
        response = self.client.post(self.login_ep, data=data, headers = headers)
        assert response.status_code == 200
