import json

import pytest
from django.urls import reverse
from user.models import User

pytest_mark = pytest.mark.django_db


@pytest.fixture
def get_token_header(django_user_model, client):
    user = django_user_model.objects.create_user(username='p1', first_name="puja", last_name="Rana",
                                                 email='pooja@gmail.com',
                                                 password='1234',mobile=1233, is_verify=True,
                                                 is_superuser=True)
    user.save()
    # login user
    url = reverse('log_in')
    data = {'username': 'p1', 'password': '1234'}
    response = client.post(url, data, content_type="application/json")

    json_data = json.loads(response.content)
    token = json_data['data']['token']
    header = {'HTTP_TOKEN': token, "content_type": "application/json"}
    return user, header

@pytest.fixture
def book_details(get_token_header):
    user, header = get_token_header
    return {
        "title":"title2",
        "price":111.00,
        "quantity":2,
        "user":user.id }

@pytest.fixture
def book_details_error(get_token_header):
    user, header = get_token_header
    return {
        "titl":"title2",
        "author":"author2",
        "price":111,
        "quantity":2,
        "user":user.id }

@pytest.fixture
def book_delete_data(client, get_token_header,book_details):
    user,header=get_token_header
    url = reverse('add_book')
    response = client.post(url, book_details, **header)
    json_data = json.loads(response.content)
    book_id = json_data['data']['id']
    url = reverse('delete_book')
    data = {'id': book_id}
    return data


class TestBookApiView:



    @pytest.mark.django_db
    def test_get_all_book_successfully(self, client, django_user_model, db):
        url = reverse('all_book')
        response = client.get(url, content_type="application/json")
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_response_as_create_book_successfully(self, client, get_token_header,book_details):
        # Create user
        user, header = get_token_header
        # Create books
        url = reverse('add_book')
        response = client.post(url, book_details, **header)
        json_data = json.loads(response.content)
        assert response.status_code == 201
        assert json_data['data']['title'] == 'title2'

    @pytest.mark.django_db
    def test_response_as_create_book_unsuccessfully(self, client, get_token_header, book_details_error):
        # Create user
        user, header = get_token_header
        # Create books
        url = reverse('add_book')
        response = client.post(url, book_details_error, **header)
        # json_data = json.loads(response.content)
        assert response.status_code == 204

    @pytest.mark.django_db
    def test_response_as_delete_books_successfully(self, client, get_token_header, book_delete_data):
        user, header = get_token_header
        url = reverse('delete_book')
        response = client.delete(url, book_delete_data, **header)
        assert response.status_code == 204