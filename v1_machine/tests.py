from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import (APIClient, APITestCase)

from mainframe.models import (Machine, OrderQueue, Product, Order)

CustomUser = get_user_model()
NUM_MACHINE = 10


class MetaMachineTests(APITestCase):
    def setUp(self):
        user = CustomUser.objects.create(
            email=f'tester@localhost.com',
            password=make_password('iamtester'),
            first_name=f'Tester',
            last_name='User',
            phone=f'0969696969'
        )
        machine = Machine.objects.create(
            uuid='d89647bf-ebdb-53c5-ae26-99d5256439c5',
            name='Ground floor of A5'
        )
        order = Order.objects.create(
            name='',
            user=user
        )
        OrderQueue.objects.create(
            uuid='941b62aa-a193-4ce2-95c4-397ea432f13f',
            order=order,
            machine=machine
        )

    def test_get_one(self):
        url = reverse('v1_machine:about')
        client = APIClient()
        response = client.get(
            url, **{
                'HTTP_X_MACHINE_UUID':
                    'uuid d89647bf-ebdb-53c5-ae26-99d5256439c5'
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_queue(self):
        url = reverse('v1_machine:order_queue')
        client = APIClient()
        response = client.get(
            url, **{
                'HTTP_X_MACHINE_UUID':
                    'uuid d89647bf-ebdb-53c5-ae26-99d5256439c5'
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_complete_order(self):
        url = reverse('v1_machine:complete_order')
        client = APIClient()
        data = {'order_uuid': '941b62aa-a193-4ce2-95c4-397ea432f13f'}
        response = client.post(
            path=url,
            data=data,
            **{
                'HTTP_X_MACHINE_UUID':
                    'uuid d89647bf-ebdb-53c5-ae26-99d5256439c5'
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
