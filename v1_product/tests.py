from django.urls import reverse
from rest_framework import status
from rest_framework.test import (APIClient, APITestCase)

from mainframe.models import Product

NUM_PRODUCT = 10


class ProductTests(APITestCase):
    def setUp(self):
        Product.objects.bulk_create(
            [
                Product(
                    image='',
                    name=f'Product {i}',
                    price=(i % 7) + 40,
                    unit=i * 20 + 300,
                    desc=''
                ) for i in range(NUM_PRODUCT)
            ]
        )

    def test_get_all(self):
        url = reverse('v1_product:all')
        client = APIClient()
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_search(self):
        url = reverse('v1_product:search') + '?key=product'
        client = APIClient()
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter(self):
        url = reverse('v1_product:filter') +'?fromprice=45&toprice=50'
        client = APIClient()
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
