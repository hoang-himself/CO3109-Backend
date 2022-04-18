from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.urls import reverse

from rest_framework import status
from rest_framework.test import (APIClient, APITestCase)

CustomUser = get_user_model()
NUM_USER = 10


class TestUser(APITestCase):
    header = dict()

    def setUp(self):
        preset_password = make_password('iamtester')
        self.users = CustomUser.objects.bulk_create(
            [
                CustomUser(
                    email=f'tester{i}@localhost.com',
                    password=preset_password,
                    first_name=f'Number{i}',
                    last_name='Tester',
                    phone=f'0969696969{i}'
                ) for i in range(NUM_USER)
            ]
        )

        url = reverse('v1_account:sign_in')
        client = APIClient()
        data = {'email': 'tester0@localhost.com', 'password': 'iamtester'}
        response = client.post(url, data=data)
        token = response.data.get('access_token', None)
        self.assertIsNotNone(token)
        self.header = {'HTTP_AUTHORIZATION': f'JWT {token}'}

    def test_sign_up(self):
        url = reverse('v1_account:sign_up')
        client = APIClient()
        data = {
            'email': 'user@localhost.com',
            'password': 'iamuser',
            'first_name': 'Rick',
            'last_name': 'Astley',
            'phone': '0969696969'
        }
        response = client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_one(self):
        url = reverse('v1_account:about')
        client = APIClient()
        response = client.get(url, **self.header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_sign_out(self):
        url = reverse('v1_account:sign_out')
        client = APIClient()
        response = client.delete(url, **self.header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
