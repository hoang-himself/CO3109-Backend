from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import (APIClient, APITestCase)
from rest_framework import status

from mainframe.models import (Machine, Product, Order, OrderItem)

CustomUser = get_user_model()
NUM_MACHINE = 10


class OrderTests(APITestCase):
    header = dict()

    def setUp(self):
        user = CustomUser.objects.create(
            email=f'tester@localhost.com',
            password=make_password('iamtester'),
            first_name=f'Tester',
            last_name='User',
            phone=f'0969696969',
        )
        order = Order.objects.create(
            uuid='a79da10c-8897-4f10-9107-848df79a22b5', name='', user=user
        )
        item = Product.objects.create(
            uuid='3964ff86-161f-4bcf-a211-0f2dd5f91812',
            image='',
            name=f'Sample product',
            price=47,
            unit='335mL',
            desc=''
        )
        Machine.objects.create(
            uuid='d89647bf-ebdb-53c5-ae26-99d5256439c5',
            name='Ground floor of A5'
        )
        OrderItem.objects.create(order=order, item=item, quantity=2)
        url = reverse('v1_account:sign_in')
        client = APIClient()
        data = {'email': 'tester@localhost.com', 'password': 'iamtester'}
        response = client.post(url, data=data)
        token = response.data.get('access_token', None)
        self.assertIsNotNone(token)
        self.header = {'HTTP_AUTHORIZATION': f'JWT {token}'}

    def test_get_orders(self):
        url = reverse('v1_order:self_orders')
        client = APIClient()
        response = client.get(url, **self.header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_view_order(self):
        url = reverse(
            'v1_order:view'
        ) + '?uuid=a79da10c-8897-4f10-9107-848df79a22b5'
        client = APIClient()
        response = client.get(url, **self.header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_new_order(self):
        url = reverse('v1_order:edit')
        client = APIClient()
        data = {
            "name": "huh",
            "item_uuid": "3964ff86-161f-4bcf-a211-0f2dd5f91812",
            "quantity": "3"
        }
        response = client.put(url, data, **self.header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_edit_item_in_order(self):
        url = reverse('v1_order:edit')
        client = APIClient()
        data = {
            "uuid": "a79da10c-8897-4f10-9107-848df79a22b5",
            "item_uuid": "3964ff86-161f-4bcf-a211-0f2dd5f91812",
            "quantity": "69"
        }
        response = client.put(url, data, **self.header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_item_in_order(self):
        url = reverse('v1_order:edit')
        client = APIClient()
        data = {
            "uuid": "a79da10c-8897-4f10-9107-848df79a22b5",
            "item_uuid": "3964ff86-161f-4bcf-a211-0f2dd5f91812",
            "quantity": "0"
        }
        response = client.put(url, data, **self.header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_order(self):
        url = reverse('v1_order:delete')
        client = APIClient()
        data = {'uuid': 'a79da10c-8897-4f10-9107-848df79a22b5'}
        response = client.delete(url, data, **self.header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_checkout(self):
        url = reverse('v1_order:checkout')
        client = APIClient()
        data = {
            'order_uuid': 'a79da10c-8897-4f10-9107-848df79a22b5',
            'machine_uuid': 'd89647bf-ebdb-53c5-ae26-99d5256439c5'
        }
        response = client.put(url, data, **self.header)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
