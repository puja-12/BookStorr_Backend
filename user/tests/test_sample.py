import pytest
from django.urls import reverse

pytest_mark = pytest.mark.django_db

class TestRegistrationAndLoginApiView:

    @pytest.mark.django_db
    def test_as_login_successfully(self, client, django_user_model):
        user = django_user_model.objects.create_user(username='pooja', email='pooja@gmail.com',
                                                     mobile=123456789,
                                                     password='12345678',is_verify=True)
        url = reverse('log_in')
        data = {'username':'pooja', 'password': '12345678'}
        response = client.post(url, data, content_type="application/json")
        # assert response.status_code == 200
        assert response.data['message'] =='Login success'

    @pytest.mark.django_db
    def test_as_login_unsuccessful(self, client, django_user_model):
        user = django_user_model.objects.create_user(username='pooja', email='pooja@gmail.com',
                                                     mobile=123456789,
                                                     password='12345678')
        url = reverse('log_in')
        data = {'username': 'pooja@gmail.com', 'password': '12345678'}
        response = client.post(url, data, content_type="application/json")
        assert response.status_code == 401

    @pytest.mark.django_db
    def test_as_registration_successfully(self, client, django_user_model):
        url = reverse('register_api')
        data = {'username': 'pooja', 'email': 'pooja@gmail.com', 'mobile': '45612378',
                'password': '12345678'}
        response = client.post(url, data, format='json', content_type="application/json")
        assert response.status_code == 201

    @pytest.mark.django_db
    def test_as_registration_unsuccessful(self, client, django_user_model):
        url = reverse('register_api')
        data = {'username': 'pooja', 'mobile': '45612378',
                'password': '12345678'}
        response = client.post(url, data, format='json', content_type="application/json")
        assert response.status_code == 400

