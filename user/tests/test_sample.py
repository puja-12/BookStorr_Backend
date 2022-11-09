import pytest
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from user.models import User
from django.urls import reverse


class TestLoginRegistrationModel(TestCase):
    """
    test class for testing User model
    """
    def test_should_create_user(self):
        User.objects.create_user(username='Pooja', email='pujarana@gmail.com', mobile=1234567890,
                                        password='12345678')

        assert User.objects.count() == 1

class TestLoginRegistrationView(TestCase):
    """
    Test class for User Login and Registration view
    """
    def test_create_user_with_correct_data(self):
        """
        Test function for testing user registration with correct data
        """
        url = reverse('register_api')
        data = {'username': 'pooja', 'email': 'pooja@gmail.com', 'mobile': '123456789',
                'password': 'test@123'}
        response = self.client.post(url, data, format='json', content_type="application/json")
        assert response.status_code == 201
        assert response.data['message'] == 'Register successfully,Please verified your Email'

    def test_create_user_with_incorrect_data(self):
            """
            Test function for testing user registration View with incorrect data
            """
            url = reverse('register_api')
            data = {'email': 'puja@gmail.com', 'mobile': '123455678',
                    'password': 'test@123'}
            response = self.client.post(url, data, format='json', content_type="application/json")
            assert response.status_code == 400

    def test_login_with_correct_input_success(self):
            """
            Test function for testing User Login view with correct data
            """
            credentials={'username':'pooja', 'email':'puja@gmail.com', 'mobile':123456789,
                                     'password':'test@123'}
            User.objects.create_user(**credentials)
            url = reverse('log_in')
            data = { 'email':'puja@gmail.com', 'password': 'test@123'}
            response = self.client.post(url, data, content_type="application/json")
            # assert response.status_code == 200
            assert response.data['message'] == 'Login Success'

    def test_login_with_incorrect_input_success(self):
        """
        Test function for testing user login View with incorrect data
        """
        credentials = {'username': 'pooja', 'email': 'puja@gmail.com', 'mobile': 123456789,
                       'password': 'test@123'}
        User.objects.create_user(**credentials)
        url = reverse('log_in')
        login_data = {
            'email': 'admin@gmail.com',
            'password': '1234567'}
        response = self.client.post(url, login_data, follow=True)
        assert response.status_code == 401