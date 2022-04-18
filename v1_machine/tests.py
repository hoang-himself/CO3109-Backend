from django.urls import reverse
from rest_framework import status
from rest_framework.test import (APIClient, APITestCase)

from mainframe.models import Machine

NUM_MACHINE = 10


class MetaMachineTests(APITestCase):
    def setUp(self):
        Machine.objects.create(
            uuid='d89647bf-ebdb-53c5-ae26-99d5256439c5',
            name='Ground floor of A5'
        )
        Machine.objects.bulk_create(
            [Machine(name=f'Machine {i}') for i in range(NUM_MACHINE - 1)]
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
