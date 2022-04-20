from django.contrib.auth.hashers import make_password
from django.urls import reverse
from rest_framework import status
from rest_framework.test import (APIClient, APITestCase)

from mainframe.models import (CustomUser, Order, Machine, Product)

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
        item = Product.objects.create(
            uuid='3964ff86-161f-4bcf-a211-0f2dd5f91812',
            image='',
            name=f'Sample product',
            price=47,
            unit='335mL',
            desc=''
        )
        machine = Machine.objects.create(
            uuid='7ba89104-9712-4654-b1fd-13afaa182c2b',
            name='Ground floor of A5'
        )
        Order.objects.create(
            user=user, item=item, machine=machine, order_id=69, quantity=420
        )
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
        url = reverse('v1_order:view') + '?order_id=69'
        client = APIClient()
        response = client.get(url, **self.header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_set_quantity(self):
        url = reverse('v1_order:item_quantity')
        client = APIClient()
        data = {
            'order_id': 69,
            'item_uuid': '3964ff86-161f-4bcf-a211-0f2dd5f91812',
            'new_quantity': 4
        }
        response = client.put(url, data, **self.header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_order(self):
        url = reverse('v1_order:delete')
        client = APIClient()
        data = {
            'order_id': 69,
        }
        response = client.delete(url, data, **self.header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_set_machine(self):
        url = reverse('v1_order:checkout')
        client = APIClient()
        data = {
            'order_id': 69,
            'machine_uuid': '7ba89104-9712-4654-b1fd-13afaa182c2b'
        }
        response = client.put(url, data, **self.header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
