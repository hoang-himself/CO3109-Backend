from django.urls import reverse
from rest_framework import status
from rest_framework.test import (APIClient, APITestCase)


class HeartbeatTests(APITestCase):
    def test_main_ping(self):
        url = reverse('mainframe:ping')
        client = APIClient()
        response = client.get(url)
        serializer = {'detail': 'pong'}

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer)
