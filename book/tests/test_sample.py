import pytest
import json
from django.urls import reverse
from user.models import User


@pytest.mark.django_db
def test_get_all_book_successfully(self, client, django_user_model, db):
    url = reverse('all_book/')
    response = client.get(url, content_type="application/json")
    assert response.status_code == 200



@pytest.mark.django_db
def test_add_book_correct_data(self, client, django_user_model, db):
    """
    Test function for testing add book with correct data
    """
    user = User.objects.create_superuser(username='p1', email='pujarana179@gmail.com', mobile_no='1234567',
                                         password='test@123')
    url = reverse('log_in/')
    data = {'email': 'pujarana179@gmail.com', 'password': 'test@123'}
    response = client.post(url, data, format='json')
    token = response.data['data']['token'].decode('utf-8')

    url2 = reverse('add/')
    data2 = {'title':'My Country',
             'price': 99.99, 'quantity': 5}
    header = {'Content-Type': 'application/json', 'HTTP_AUTHORIZATION':  token}
    response2 = client.post(url2, data2, **header)
    assert response2.status_code == 201

