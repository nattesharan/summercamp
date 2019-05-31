from django.test import Client
import pytest
import json
from django.contrib.auth.models import User, Group

@pytest.mark.django_db
class TestUserRegistration:
    client = Client()
    base_ep = '/api/v1/'
    signup_ep = '{}{}'.format(base_ep, 'signup/')
    def test_registration(self, groups):
        assert User.objects.count() == 0
        headers = {'Content-type': 'application/json'}
        data = {
            'first_name': 'test',
            'last_name': 'user',
            'username': 'testme',
            'password1': 'test1',
            'password2': 'test1',
            'email': 'test1@gmail.com',
            'description': 'test',
            'city': 'Test city',
            'age': 23,
            'phone': '9765812345',
            'gender': 'M',
            'role': Group.objects.first().pk
        }
        response = self.client.post(self.signup_ep, data=data, headers = headers)
        assert response.status_code == 200
        response_data = response.json()
        assert response_data['success']
        assert User.objects.count() == 1
    
    def test_registration_missing_fields(self, groups):
        headers = {'Content-type': 'application/json'}
        data = {
            'last_name': 'user',
            'username': 'testme',
            'password1': 'test1',
            'password2': 'test1',
            'email': 'test1@gmail.com',
            'description': 'test',
            'city': 'Test city',
            'age': 23,
            'phone': '9765812345',
            'gender': 'M',
            'role': Group.objects.first().pk
        }
        response = self.client.post(self.signup_ep, data=data, headers = headers)
        assert response.status_code == 400
    
    def test_registration_password_mismatch(self, groups):
        headers = {'Content-type': 'application/json'}
        data = {
            'first_name': 'test',
            'last_name': 'user',
            'username': 'testme',
            'password1': 'test1',
            'password2': 'test11212',
            'email': 'test1@gmail.com',
            'description': 'test',
            'city': 'Test city',
            'age': 23,
            'phone': '9765812345',
            'gender': 'M',
            'role': Group.objects.first().pk
        }
        response = self.client.post(self.signup_ep, data=data, headers = headers)
        assert response.status_code == 400
    
    def test_invalid_gender(self, groups):
        headers = {'Content-type': 'application/json'}
        data = {
            'first_name': 'test',
            'last_name': 'user',
            'username': 'testme',
            'password1': 'test1',
            'password2': 'test1',
            'email': 'test1@gmail.com',
            'description': 'test',
            'city': 'Test city',
            'age': 23,
            'phone': '9765812345',
            'gender': 'K',
            'role': Group.objects.first().pk
        }
        response = self.client.post(self.signup_ep, data=data, headers = headers)
        assert response.status_code == 400
    
    def test_invalid_role(self, groups):
        headers = {'Content-type': 'application/json'}
        data = {
            'first_name': 'test',
            'last_name': 'user',
            'username': 'testme',
            'password1': 'test1',
            'password2': 'test1',
            'email': 'test1@gmail.com',
            'description': 'test',
            'city': 'Test city',
            'age': 23,
            'phone': '9765812345',
            'gender': 'K',
            'role': "ABC"
        }
        response = self.client.post(self.signup_ep, data=data, headers = headers)
        assert response.status_code == 400

    def test_registration_duplicate_user(self, groups):
        headers = {'Content-type': 'application/json'}
        data = {
            'first_name': 'test',
            'last_name': 'user',
            'username': 'testme',
            'password1': 'test1',
            'password2': 'test1',
            'email': 'test1@gmail.com',
            'description': 'test',
            'city': 'Test city',
            'age': 23,
            'phone': '9765812345',
            'gender': 'M',
            'role': Group.objects.first().pk
        }
        response = self.client.post(self.signup_ep, data=data, headers = headers)
        assert response.status_code == 200
        data = {
            'first_name': 'test123',
            'last_name': 'user123',
            'username': 'testme',
            'password1': 'test1111',
            'password2': 'test1111',
            'email': 'test121@gmail.com',
            'description': 'test',
            'city': 'Test city',
            'age': 23,
            'phone': '9765812345',
            'gender': 'F',
            'role': Group.objects.first().pk
        }
        response = self.client.post(self.signup_ep, data=data, headers = headers)
        assert response.status_code == 400
